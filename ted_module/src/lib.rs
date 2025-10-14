use pyo3::prelude::*;

use std::collections::HashMap;

struct CanonicalLabel {
    clade : Vec<usize>,
    rank : usize
}

impl CanonicalLabel {
    fn to_string(&self) -> String {
        let mut return_string : String = "".to_owned();
        for label in &self.clade {
            return_string.push_str((*label).to_string().as_str());
        }
        return_string.push('-');
        return_string.push_str(self.rank.to_string().as_str());
        return return_string;
    }
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

/// The same_clade function assumes the clades are sorted
/// They are sorted during the construction of the Graph-s.
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

    fn canonical_form(&self) -> HashMap<String, Vec<String>> {
        
    // finding root
    let roots : Vec<usize> = self.in_ngbh
        .iter()
        .filter(|(_,&ref in_ngbhood)| (*in_ngbhood).len()==0)
        .map(|(node,_)| *node)
        .collect();

    assert!(roots.len()==1);
    let root = roots[0];


    let mut cano_label_map : HashMap<usize, CanonicalLabel> = HashMap::new();

    cano_label_map.insert(root, CanonicalLabel { clade : self.clade.get(&root).unwrap().to_vec(), rank : 0 });

    let mut queue : Vec<usize> = vec![root];

    while queue.len() > 0 {
        let node : usize = queue.pop().unwrap();

        for child in self.out_ngbh.get(&node).unwrap() {
            if self.is_tree_edge(node, *child) {
                let canonical_label : &CanonicalLabel = cano_label_map.get(&node).unwrap();

                if same_clade(self.clade.get(&node).unwrap(), self.clade.get(&child).unwrap()) {
                    cano_label_map.insert(*child, CanonicalLabel {clade : canonical_label.clade.clone() , rank : canonical_label.rank+1});
                }
                else {
                    cano_label_map.insert(*child, CanonicalLabel {clade : self.clade.get(&child).unwrap().to_vec() , rank : 0});
                }
                queue.push(*child);
            }
        }
    }
    
    let mut canonical_form : HashMap<String,Vec<String>> = HashMap::new();
    
    for (node, neighborhood) in self.out_ngbh.iter() {
        for node2 in neighborhood {
            if !self.is_tree_edge(*node, *node2) {
                
                let cano_label1 = cano_label_map.get(&node).unwrap().to_string();
                let cano_label2 = cano_label_map.get(&node2).unwrap().to_string();

                if let Some(v) = canonical_form.get_mut(&cano_label1) {
                    (*v).push(cano_label2);
                }
                else {
                    canonical_form.insert(cano_label1, vec![cano_label2]);
                }
            }
        }
    }

    for (_, val) in canonical_form.iter_mut() {
        (*val).sort();
    }

    return canonical_form;

    }

    fn is_iso(&self, other_graph : Graph) -> bool {
        let cano1 : HashMap<String, Vec<String>> = self.canonical_form();
        let cano2 : HashMap<String, Vec<String>> = other_graph.canonical_form();

        for (cano_label1, neighborhood1) in cano1.iter() {

            if let Some(neighborhood2) = cano2.get(cano_label1) {
               // now test that neighborhood1 and neighborhood2 are equal.
               if neighborhood1.len()!=neighborhood2.len() {
                   return false;
               }

               for k in 0..neighborhood1.len() {
                   if neighborhood1[k] != neighborhood2[k] {
                       return false;
                   }
               }
            }
            else {
                return false;
            }
        }
        return true;
    }

    fn remove_transfer_set(&self, transfers_to_remove : &Vec<&(usize,usize)>) -> Graph {
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

        // the edge_label of new edge is set, the old edge is removed
        self.edge_label.remove(&(tree_parent, node));
        for tree_child in &tree_children {
            self.edge_label.remove(&(node,*tree_child));
            self.edge_label.insert((tree_parent,*tree_child), EdgeType::TREE); 
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
        println!("{:?}", self.edge_label);
        println!("{:?} {:?}", u,v);
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

        new_clade.sort();
        graph.clade.insert(node, new_clade.clone());
        return new_clade;
    }

    fill_clade_map(root, &mut graph);

    return graph;

}

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
fn transfer_edition_distance(network1 : Vec<String>, network2 : Vec<String>) -> PyResult<usize> {
    let mut graph1 : Graph = parse_graph(network1);
    let mut graph2 : Graph = parse_graph(network2);

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
            let graph1p : Graph = graph1.remove_transfer_set(&v1);
            let graph2p : Graph = graph2.remove_transfer_set(&v2);
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
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_to_string() {
        let cano_label : CanonicalLabel = CanonicalLabel {clade : vec![1,2,3], rank : 8};
        assert_eq!(cano_label.to_string(),"123-8".to_string());
    }

    #[test]
    fn test_same_clade() {
        let v1 : Vec<usize> = vec![1,2,3];
        let v2 : Vec<usize> = vec![1,3];
        let v3 : Vec<usize> = vec![1,3,4];
        assert!(same_clade(&v1,&v1));
        assert!(same_clade(&v2,&v2));
        assert!(same_clade(&v3,&v3));
        assert!(!same_clade(&v1,&v2));
        assert!(!same_clade(&v1,&v3));
        assert!(!same_clade(&v2,&v3));
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn ted_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(transfer_edition_distance,m)?)?;
    Ok(())
}

