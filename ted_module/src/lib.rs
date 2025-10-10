use pyo3::prelude::*;

use std::collections::HashMap;

#[derive(Default)]
struct NetworkNode {
    label : usize,
    clade : Vec<usize>,
    tree_children: Vec<NetworkNode>,
    transfer_out_ngbh : Vec<NetworkNode>,
    canonical_label : String
}

struct CanonicalLabel {
    clade : &Vec<usize>,
    rank : usize
}

#[derive(PartialEq,Debug,Clone)]
enum EdgeType {
    TRANSFER,
    TREE,
}

#[derive(Default,Debug)]
struct Graph {
    out_ngbh : HashMap<usize, Vec<usize>>,
    in_ngbh : HashMap<usize, Vec<usize>>,
    edge_label: HashMap<(usize, usize), EdgeType>, 
    clade : HashMap<usize, Vec<usize>> 
}

fn same_clade(clade1 : &Vec<usize>, clade2 : &Vec<usize>) -> bool {
    if clade1.len() != clade2.len() {
        return false;
    }
    for k in 0..clade1.len() {
        if clade1[k] != clade2[k] {
            return false;
        }
    }
    return true;
}

impl Graph {

    fn canonical_form(&self) -> HashMap<CanonicalLabel, Vec<CanonicalLabel>> {
        
    // finding root
    let roots : Vec<usize> = graph.in_ngbh
        .iter()
        .filter(|(_,&ref in_ngbhood)| (*in_ngbhood).len()==0)
        .map(|(node,_)| *node)
        .collect();

    assert!(roots.len()==1);
    let root = roots[0];

    let mut canonical_form : HashMap<CanonicalLabel,Vec<CanonicalLabel>> = HashMap::new();

    let mut cano_label_map : HashMap<usize, CanonicalLabel> = HashMap::new();

    cano_label_map.insert(root, CanonicalLabel { clade : self.clade.get(&root).unwrap(), rank : 0 })

    let mut queue : Vec<usize> = vec![root];

    while queue.len() > 0 {
        let node : usize = queue.pop();

        for child in self.out_ngbh.get(&node).unwrap() {
            if is_tree_edge(node, child) {
                let canonical_label : CanonicalLabel = cano_label_map.get(&node).unwrap();

                if same_clade(self.clade.get(&node).unwrap(), self.clade.get(&child).unwrap()) {
                    cano_label_map.insert(child, CanonicalLabel {clade : canonical_label.clade , rank : canonical_label.rank+1});
                }
                else {
                    cano_label_map.insert(child, CanonicalLabel {clade : self.clade.get(&root).unwrap() , rank : 0});
                }
                queue.push(child);
            }
        }
    }
    
    for (node, neighborhood) in self.out_ngbh.iter() {
        for node2 in neighborhood {
            if !self.is_tree_edge(node, node2) {
                
                cano_label1 = cano_label_map.get(&node).unwrap();
                cano_label2 = cano_label_map.get(&node2).unwrap();

                if let Some(v) = canonical_form.get_mut(&cano_label1) {
                    *v.push(cano_label2);
                }
                else {
                    canonical_form.insert(cano_label1, vec![cano_label2]);
                }
            }
        }
    }

    return canonical_form;
    }

    fn is_iso(&self, other_graph : Graph) -> bool {
        let cano1 : Vec<(usize,usize)> = self.canonical_form();
        let cano2 : Vec<(usize,usize)> = other_graph.canonical_form();

        // TODO test they are the same. beware of order of things ! same applies for "same_clade"
        // function btw.
    }

    fn remove_transfer_set(&self, transfers_to_remove : Vec<&(usize,usize)>) -> Graph {
        let mut new_graph : Graph = Graph {
            in_ngbh : self.in_ngbh.clone(),
            out_ngbh : self.out_ngbh.clone(),
            edge_label : self.edge_label.clone(),
            clade : self.clade.clone(),
        };

        for (u,v) in transfers_to_remove {
            new_graph.remove_transfer(*u,*v);
        }

        new_graph.remove_degree_2_nodes();

        return new_graph;
    }

    fn remove_transfer(&mut self, u : usize, v : usize) {
        assert!(*self.edge_label.get(&(u,v)).unwrap()==EdgeType::TRANSFER);

        let out_neighborhood : &mut Vec<usize> = self.out_ngbh.get_mut(&u).unwrap(); 
        out_neighborhood.retain(|value| *value != v);

        let in_neighborhood : &mut Vec<usize> = self.in_ngbh.get_mut(&v).unwrap(); 
        in_neighborhood.retain(|value| *value != u);
    }

    fn remove_degree_2_nodes(&mut self) {

        let nodes : Vec<usize> = self.clade.keys().cloned().collect();

        for node in nodes {
            if self.in_ngbh.get(&node).unwrap().len()==1 {
                if self.out_ngbh.get(&node).unwrap().len()==1 {
                    self.remove_node(node);
                }
            }
        }
        
    }

    fn list_transfers(&self) -> Vec<(usize,usize)> {

        let mut return_value : Vec<(usize,usize)> = Vec::new();

        for (node, out_neighborhood) in self.out_ngbh.iter() {
            for neighbor in out_neighborhood {
                if !self.is_tree_edge(*node, *neighbor) {
                    return_value.push((*node,*neighbor));
                }
            }
        }

        return return_value;
    }

    fn remove_clade(&mut self, clade_to_remove : &Vec<usize>) -> usize {

        let mut nops : usize = 0;

        let nodes : Vec<usize> = self.clade.keys().cloned().collect();

        for node in nodes {
            let clade : &Vec<usize> = self.clade.get(&node).unwrap();
            if same_clade(clade_to_remove, clade) {
                nops += self.remove_node(node);
            }
        }

        return nops;
    }

    /// 
    ///  remove_node assumes the network is binary !!!!
    /// 
    fn remove_node(&mut self, node : usize) -> usize {

        // find tree parent and tree children
        let mut tree_parents : Vec<usize> = Vec::new();
        let mut tree_children : Vec<usize> = Vec::new();
        for in_neighbor in self.in_ngbh.get(&node).unwrap() {
            if self.is_tree_edge(*in_neighbor, node) {
                tree_parents.push(*in_neighbor);
            }
        }
        assert!(tree_parents.len()==1);
        let tree_parent : usize = *tree_parents.get(0).unwrap();
        for out_neighbor in self.out_ngbh.get(&node).unwrap() {
            if self.is_tree_edge(node, *out_neighbor) {
                tree_children.push(*out_neighbor);
            }
        }

        // the tree children become children of the tree parent
        for tree_child in &tree_children {
            let tree_child_in_ngbh : &mut Vec<usize> = self.in_ngbh.get_mut(tree_child).unwrap();
            tree_child_in_ngbh.push(tree_parent);
        }

        // the tree parent becomes parent of tree children
        let tree_parent_out_ngbh : &mut Vec<usize> = self.out_ngbh.get_mut(&tree_parent).unwrap();
        for tree_child in &tree_children {
            tree_parent_out_ngbh.push(*tree_child);
        }

        // the neighborhoods of other nodes are filtered to remove node
        for in_ngbhood in self.in_ngbh.values_mut() {
            in_ngbhood.retain(|value| *value != node);
        }

        for out_ngbhood in self.out_ngbh.values_mut() {
            out_ngbhood.retain(|value| *value != node);
        }

        // bye bye node
        self.in_ngbh.remove_entry(&node);
        self.out_ngbh.remove_entry(&node);
        self.clade.remove_entry(&node);

        return 1;
    }

    fn has_clade(&self, test_clade : &Vec<usize>) -> bool {
        for clade in self.clade.values() {
            if same_clade(test_clade, clade) {
                return true;
            }
        }
        return false;
    }

    fn list_clades(&self) -> Vec<Vec<usize>> {
        let mut return_value : Vec<Vec<usize>> = Vec::new();

        for (node, clade) in self.clade.iter() {
            // to ensure a clade is only returned once,
            // we only add "clade" to the return value
            // if node has a different clade from its
            // tree children. To add it only once
            // we only check one tree child.
            for child in self.out_ngbh.get(&node).unwrap() {
                if self.is_tree_edge(*node,*child) {
                    if !same_clade(clade, self.clade.get(child).unwrap()) {
                        return_value.push(clade.clone());
                        break;
                    }
                }
            }
        }
        return return_value;
    }

    fn is_tree_edge(&self, u : usize, v : usize) -> bool {
        *self.edge_label.get(&(u,v)).unwrap()==EdgeType::TREE 
    }
}

fn parse_graph(list_edges : Vec<String>) -> Graph {

    let mut graph : Graph = Graph {
        out_ngbh : HashMap::new(),
        in_ngbh : HashMap::new(),
        edge_label : HashMap::new(),
        clade : HashMap::new(),
    };

    for line in list_edges {
        let elements : Vec<&str> = line.split_whitespace().collect();
        let u : usize = elements[0].parse().unwrap();
        let v : usize = elements[1].parse().unwrap();

        // insert v as out ngbh of u
        if let Some(vec) = graph.out_ngbh.get_mut(&u) {
            vec.push(v);
        }
        else {
            graph.out_ngbh.insert(u, vec![v]);
        }

        // insert u as out ngbh of v
        if let Some(vec) = graph.in_ngbh.get_mut(&v) {
            vec.push(u);
        }
        else {
            graph.in_ngbh.insert(v, vec![u]);
        }

        // make sure u and v have (possibly empty) ngbhs nonetheless
        graph.in_ngbh.entry(u).or_insert(Vec::new());
        graph.in_ngbh.entry(v).or_insert(Vec::new());
        graph.out_ngbh.entry(v).or_insert(Vec::new());
        graph.out_ngbh.entry(u).or_insert(Vec::new());

        let edge_type: EdgeType = match elements[2] {
            "tree" => EdgeType::TREE,
            "transfer" => EdgeType::TRANSFER,
            _ => panic!("not a known type"),
        };
        graph.edge_label.insert((u,v), edge_type);
    }

    // find root 
    let roots : Vec<usize> = graph.in_ngbh
        .iter()
        .filter(|(_,&ref in_ngbhood)| (*in_ngbhood).len()==0)
        .map(|(node,_)| *node)
        .collect();

    println!("{:?}", graph);
    println!("{:?}", roots);
    assert!(roots.len()==1);
    let root = roots[0];

    fn fill_clade_map(node : usize, graph : &mut Graph) -> Vec<usize> {

        let out_neighbors = graph.out_ngbh.get(&node).unwrap().clone();

        if out_neighbors.len() == 0 {
            graph.clade.insert(node, vec![node]); 
            return vec![node];
        }

        let mut new_clade : Vec<usize> = Vec::new();

        for child in out_neighbors {
            if *graph.edge_label.get(&(node,child)).unwrap()==EdgeType::TREE {
                let child_clade : Vec<usize> = fill_clade_map(child, graph);
                for v in child_clade {
                    new_clade.push(v);
                }
            }
        }

        graph.clade.insert(node, new_clade.clone());
        return new_clade;
    }

    fill_clade_map(root, &mut graph);

    return graph;

}

//fn make_network(list_edges : Vec<String>) -> NetworkNode {
//
//    // make graph from list of edges
//    graph = parse_graph(list_edges);
//
//    // find root 
//    let roots : Vec<usize> = graph.in_ngbh
//        .iter()
//        .filter(|(_,&ref in_ngbhood)| (*in_ngbhood).len()==0)
//        .map(|(node,_)| *node)
//        .collect();
//
//    assert!(roots.len()==1);
//    let root = roots[0];
//
//    // recursive function whose main purpose is to label
//    // by clades
//    fn network_node_creation(node_label : usize, 
//        out_neighborhood : &HashMap<usize, Vec<usize>>,
//        edge_label : &HashMap<(usize,usize), EdgeType>) -> NetworkNode {
//
//        let out_neighbors = out_neighborhood.get(&node_label).unwrap();
//
//        if out_neighbors.len() == 0 {
//            return NetworkNode { 
//                label : node_label,
//                clade : vec![node_la bel],
//                tree_children : Vec::new(),
//                ..Default::default()
//            };
//        }
//        
//        let mut new_clade : Vec<usize> = Vec::new();
//        let mut children_vec : Vec<NetworkNode> = Vec::new();
//        for child in out_neighbors {
//            if edge_label.get(&(node_label,*child)).unwrap()==EdgeType::TREE {
//                let node_child : NetworkNode = network_node_creation(*child, 
//                                                                out_neighborhood,
//                                                                edge_label);
//                for v in &node_child.clade {
//                    new_clade.push(*v);
//                }
//                insert_ordered_by_clade(children_vec, node_child);
//            }
//        }
//        
//        return NetworkNode {
//            label : node_label,
//            clade : new_clade,
//            tree_children : children_vec,
//            ..Default::default()
//        };
//    }
//
//    // original call to get clades
//    let tree_node_root : NetworkNode = network_node_creation(root, &graph.out_ngbh, &graph.edge_label);
//
//    // no choice but to store a correspondance from label to node
//    let mut label_to_network_node : HashMap<usize, NetworkNode> = HashMap::new();
//
//    let mut queue : Vec<NetworkNode> = vec![tree_node_root];
//    tree_node_root.canonical_label = CanonicalLabel { clade : tree_root_node.clade , rank : 0}; 
//    label_to_network_node.insert(tree_node_root.label, tree_node_root);
//
//    while queue.len() > 0 {
//        let node : NetworkNode = queue.pop();
//        label_to_network_node.insert(node.label, node);
//
//        for tree_child in node.tree_children {
//            if equal_clades(node.clade, tree_child.clade) {
//                tree_child.canonical_label = CanonicalLabel { clade : tree_child.clade, rank : node.canonical_label.rank + 1 };
//            }
//            else {
//                tree_child.canonical_label = CanonicalLabel { clade : tree_child.clade, rank : 0 };
//            }
//            queue.push(tree_child);
//        }
//    }
//
//    let mut queue : Vec<NetworkNode> = vec![tree_node_root];
//
//    while queue.len() > 0 {
//        let node : NetworkNode = queue.pop();
//
//        for v in graph.out_ngbh.get(node.label) {
//            if &graph.edge_type.get((node.label,v)).unwrap()==EdgeType::TRANSFER {
//                node.transfer_out_ngbh.push(label_to_network_node(v));
//            }
//        }
//
//        for tree_child in node.tree_children {
//            queue.push(tree_child);
//        }
//    }
//
//    return tree_node_root; 
//}
//
//fn equal_clades(clade1 : &Vec<usize>, clade2 : &Vec<usize>) -> bool {
//    if clade1.len()!=clade2.len() {
//        return false;
//    }
//    for k in 0..=clade.len() {
//        if clade1[k]!=clade2[k] {
//            return false;
//        }
//    }
//    return true;
//}
//
//fn insert_ordered_by_clade(node_vec, node) -> Vec<NetworkNode> {
//    for k in 0..node_vec.len() {
//        if is_smaller_clade(node.clade, node_vec[k].clade) {
//            node_vec.insert(k,node);
//        }
//    }
//    return node_vec
//}
//
//"""
//Returns true if clade1 is smaller than or equal to clade2
//"""
//fn is_smaller_clade(clade1: &Vec<usize>, clade2 : &Vec<usize>) -> bool {
//    let mut k = 0;
//    loop {
//        if k >= clade1.len() {
//            return true;
//        }
//        if k >= clade2.len() {
//            return false;
//        }
//        if clade1[k] < clade2[k] {
//            return true;
//        }
//        if clade2[k] < clade1[k] {
//            return false;
//        }
//        k += 1;
//    }
//    return true;
//}
//
//fn get_clades(node: NetworkNode) -> Vec<Vec<usize>> {
//    let mut return_vec : Vec<Vec<usize>> = vec![node.clade];
//
//    for child in node.tree_children {
//        let clades = get_clades(child);
//        for clade in clades {
//            return_vec = insert_ordered_by_clade(return_vec, 
//        } 
//    }
//}
//
//fn ensure_same_base_tree(n1 : NetworkNode, n2 : NetworkNode) -> (NetworkNode, NetworkNode, usize) {
//    let mut num_ops = 0;
//
//    let vec_clades : Vec<Vec<usize>> = Vec::new();
//
//    
//
//}
//
//

fn powerset(v : &[(usize,usize)]) -> Vec<Vec<&(usize,usize)>> {
    (0..2usize.pow(v.len() as u32)).map(|i| {
        v.iter()
            .enumerate()
            .filter(|&(t,_)| (i >> t) % 2 == 1)
            .map(|(_, element)| element)
            .collect()
    }).collect()
}

#[pyfunction]
fn transfer_edition_distance(N1 : Vec<String>, N2 : Vec<String>) -> PyResult<usize> {
    let mut graph1 : Graph = parse_graph(N1);
    let mut graph2 : Graph = parse_graph(N2);

    let mut distance : usize = 0;

    // Start of block ensuring same base tree
    let clades1 : Vec<Vec<usize>> = graph1.list_clades();
    for clade1 in &clades1 {
        if !graph2.has_clade(clade1) {
            let cost : usize = graph1.remove_clade(clade1);
            distance += cost;
        }
    }

    let clades2 : Vec<Vec<usize>> = graph2.list_clades();
    for clade2 in &clades2 {
        if !graph1.has_clade(clade2) {
            let cost : usize = graph2.remove_clade(clade2);
            distance += cost;
        }
    }

    graph1.remove_degree_2_nodes();
    graph2.remove_degree_2_nodes();
    // end of block ensuring same base tree

    let transfers1 : Vec<(usize,usize)> = graph1.list_transfers(); 
    let transfers2 : Vec<(usize,usize)> = graph2.list_transfers(); 

    let mut found_it : bool = false;
    for v1 in powerset(&transfers1) {
        for v2 in powerset(&transfers2) {
            let graph1p : Graph = graph1.remove_transfer_set(v1);
            let graph2p : Graph = graph2.remove_transfer_set(v2);
            if graph1p.is_iso(graph2p) {
                distance += v1.len();
                distance += v2.len();
                found_it = true;
                break;
            }
        }
        if found_it {
            break;
        }
    }
    assert!(found_it);

    return Ok(distance);
//    return Ok(ted_distance(n1,n2))
}

/// A Python module implemented in Rust.
#[pymodule]
fn ted_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(transfer_edition_distance,m)?)?;
    Ok(())
}
