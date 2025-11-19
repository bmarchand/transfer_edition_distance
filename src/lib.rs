//! This crate contains the rust implementation  
//! (along with PyO3 python bindings) of the
//! algorithms presented in INSERTPREPRINTLINK
//! for computing distances between LGT networks.
//!
//! The crate may be used in three ways:
//! 
//! # As a python library
//! # As a command-line tool
//! # As a rust crate
//! ```
//! let network1 = vec!["1 8 tree",
//!                     "1 7 tree",
//!                     "8 6 tree",
//!                     "7 3 tree",
//!                     "6 2 tree",
//!                     "2 4 tree",
//!                     "2 9 tree",
//!                     "9 5 tree",
//!                     "6 7 transfer",
//!                     "8 9 transfer"];
//!
//! let network2 = vec!["1 6 tree",
//!                     "1 7 tree",
//!                     "6 8 tree",
//!                     "7 3 tree",
//!                     "8 2 tree",
//!                     "2 4 tree",
//!                     "2 9 tree",
//!                     "9 5 tree",
//!                     "6 7 transfer",
//!                     "8 9 transfer"];
//!
//! let d_ordered = transfer_edition_distance_rust(network1.into_iter()
//!                                                    .map(|x| x.to_string())
//!                                                    .collect(), 
//!                                                network2.into_iter()
//!                                                    .map(|x| x.to_string())
//!                                                    .collect());
//! ```
use pyo3::prelude::*;

use std::collections::HashMap;
use std::collections::HashSet;

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
    clade : HashMap<usize, Vec<usize>>,
    weight : HashMap<(usize,usize), f64>
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
        //println!("cano1 iso test {:?}", cano1);
        //println!("cano2 iso test {:?}", cano2);

        for (cano_label1, neighborhood1) in cano1.iter() {
            //println!("{:?}", cano2.get(cano_label1));
            match cano2.get(cano_label1) {
                Some(neighborhood2) => {
                    // now test that neighborhood1 and neighborhood2 are equal.
                    if neighborhood1.len()!=neighborhood2.len() {
                        return false;
                    }

                    for k in 0..neighborhood1.len() {
                        if neighborhood1[k] != neighborhood2[k] {
                            return false;
                        }
                    }
                },
                None => { return false; }
            }
        }

        for (cano_label2, neighborhood2) in cano2.iter() {
            if let Some(neighborhood1) = cano1.get(cano_label2) {
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
            weight : self.weight.clone(),
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


    /// Modifies the network to remove the clade, and returns
    /// the cost of removing this clade.
    fn remove_clade(&mut self, clade_to_remove : &Vec<usize>) -> f64 {

        let mut cost : f64 = 0f64;

        let nodes : Vec<usize> = self.clade.keys().cloned().collect();

        for node in nodes {
            let clade : &Vec<usize> = self.clade.get(&node).unwrap();
            if same_clade(clade_to_remove, clade) {
                //println!("from remove clade");
                cost += self.remove_node(node);
            }
        }

        return cost;
    }

    /// The input node is contracted into its tree parent. 
    ///
    /// Any transfer adjacent to this node is removed. 
    /// When this is the case, the weight is added to 
    /// the returned cost.
    /// 
    fn remove_node(&mut self, node : usize) -> f64 {
        //println!("removing node {:?}", node);

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

        // the edge_labels of the new edges are set
        for tree_child in &tree_children {
            self.edge_label.insert((tree_parent,*tree_child), EdgeType::TREE); 
        }

        // the tree parent becomes parent of tree children
        let tree_parent_out_ngbh : &mut Vec<usize> = self.out_ngbh.get_mut(&tree_parent).unwrap();
        for tree_child in &tree_children {
            tree_parent_out_ngbh.push(*tree_child);
        }

        // are we removing transfers ? and if so what are their weight ?
        let mut weight : f64 = 0f64;
        let mut found_transfer : bool = false;
        for in_neighbor in self.in_ngbh.get(&node).unwrap() {
            if !self.is_tree_edge(*in_neighbor, node) {
                weight += *self.weight.get(&(*in_neighbor,node)).unwrap_or(&1f64);
                found_transfer = true;
            }
        }
        for out_neighbor in self.out_ngbh.get(&node).unwrap() {
            if !self.is_tree_edge(node, *out_neighbor) {
                weight += *self.weight.get(&(node, *out_neighbor)).unwrap_or(&1f64);
                found_transfer = true;
            }
        }
        if !found_transfer {
            weight = 1f64;
        }

        // the old edge labels are removed
        self.edge_label.remove(&(tree_parent, node));
        for tree_child in &tree_children {
            self.edge_label.remove(&(node,*tree_child));
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

        return weight;
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
            let mut do_we_add_it : bool = true;
            for child in self.out_ngbh.get(&node).unwrap() {
                if self.is_tree_edge(*node,*child) {
                    if same_clade(clade, self.clade.get(child).unwrap()) {
                        do_we_add_it = false;
                        break;
                    }
                }
            }
            if do_we_add_it {
                return_value.push(clade.clone());
            }
        }
        return return_value;
    }

    fn is_tree_edge(&self, u : usize, v : usize) -> bool {
        *self.edge_label.get(&(u,v)).unwrap()==EdgeType::TREE 
    }
}

fn parse_graph_weighted(list_edges : Vec<String>) -> Graph {

    let mut graph : Graph = Graph {
        out_ngbh : HashMap::new(),
        in_ngbh : HashMap::new(),
        edge_label : HashMap::new(),
        clade : HashMap::new(),
        weight : HashMap::new(),
    };

    for line in list_edges {
   //     println!("{:?}",line);
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
        graph.edge_label.insert((u,v), edge_type.clone());

        if edge_type==EdgeType::TRANSFER {
            let weight : f64 = elements[3].parse().unwrap();
            // weight
            graph.weight.insert((u,v), weight);
        }
    }

    // find root 
    let roots : Vec<usize> = graph.in_ngbh
        .iter()
        .filter(|(_,&ref in_ngbhood)| (*in_ngbhood).len()==0)
        .map(|(node,_)| *node)
        .collect();

    assert!(roots.len()==1);
    let root = roots[0];

    fn fill_clade_map(node : usize, graph : &mut Graph) -> Vec<usize> {

        let out_neighbors = graph.out_ngbh.get(&node).unwrap().clone();

        let mut new_clade : Vec<usize> = Vec::new();

        let mut cnt_tree_children : usize = 0;
        for child in out_neighbors {
            if *graph.edge_label.get(&(node,child)).unwrap()==EdgeType::TREE {
                cnt_tree_children += 1;
                let child_clade : Vec<usize> = fill_clade_map(child, graph);
                for v in child_clade {
                    new_clade.push(v);
                }
            }
        }

        if cnt_tree_children==0 {
            graph.clade.insert(node, vec![node]); 
            return vec![node];
        }

        new_clade.sort();
        graph.clade.insert(node, new_clade.clone());
        return new_clade;
    }

    fill_clade_map(root, &mut graph);

    return graph;

}

fn parse_graph(list_edges : Vec<String>) -> Graph {

    let mut graph : Graph = Graph {
        out_ngbh : HashMap::new(),
        in_ngbh : HashMap::new(),
        edge_label : HashMap::new(),
        clade : HashMap::new(),
        weight : HashMap::new(),
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

    assert!(roots.len()==1);
    let root = roots[0];

    fn fill_clade_map(node : usize, graph : &mut Graph) -> Vec<usize> {

        let out_neighbors = graph.out_ngbh.get(&node).unwrap().clone();

        let mut no_tree_descendant : bool = true;
        for v in &out_neighbors {
            if graph.is_tree_edge(node, *v) {
                no_tree_descendant = false;
            }
        }
        if no_tree_descendant {
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

fn all_integers_with_weight_k(n : u128, k : u128) -> Vec<u128> {
    let mut result : Vec<u128> = Vec::new();
    if k==0 {
        result.push(0);
        return result;
    }

    let mut set : u128 = (1 << k) - 1;
    let limit : u128 = 1 << n;

    while set < limit 
    {
        result.push(set);
        let c : u128 = set & set.wrapping_neg();
        let r : u128 = set + c;
        //println!("c {:?}",c);
        set = ((( r ^ set ) >> 2) / c ) |  r;
    }
    return result;
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

pub fn transfer_edition_distance_unordered_weighted_rust(network1: Vec<String>, network2 : Vec<String>) -> f64 {

    let mut graph1 : Graph = parse_graph_weighted(network1);
    let mut graph2 : Graph = parse_graph_weighted(network2);

    let mut distance : f64 = 0f64;

    // Start of block ensuring same base tree
    let clades1 : Vec<Vec<usize>> = graph1.list_clades();
    for clade1 in &clades1 {
        if !graph2.has_clade(clade1) {
            let cost : f64 = graph1.remove_clade(clade1);
            distance += cost;
        }
    }

    let clades2 : Vec<Vec<usize>> = graph2.list_clades();
    for clade2 in &clades2 {
        if !graph1.has_clade(clade2) {
            let cost : f64 = graph2.remove_clade(clade2);
            distance += cost;
        }
    }

    graph1.remove_degree_2_nodes();
    graph2.remove_degree_2_nodes();
    // end of block ensuring same base tree


    let clades1 : Vec<Vec<usize>> = graph1.list_clades();
    let clades2 : Vec<Vec<usize>> = graph2.list_clades();
    //println!("clades1 {:?}", clades1);

    // associating an integer id to every clade
    let mut clade_id : HashMap<Vec<usize>, usize> = HashMap::new();
    let mut id: usize = 0;
    for clade1 in &clades1 {
        clade_id.insert(clade1.clone(), id);
        id += 1
    }

    for clade2 in &clades2 {
        match clade_id.get(clade2) {
            Some(_) => {},
            None => {
                clade_id.insert(clade2.clone(), id);
                id += 1;
            }, 
        }
    }
    //println!("clade_id {:?}", clade_id);

    // weight1: (id1, id2) -> weight
    let mut weight1: HashMap<(usize, usize), f64> = HashMap::new();
    let mut weight2: HashMap<(usize, usize), f64> = HashMap::new();

    let mut transfer_ids: HashSet<(usize,usize)> = HashSet::new();

    for (u1,v1) in graph1.list_transfers() {
        let clade_u1  = graph1.clade.get(&u1).unwrap();
        let clade_v1  = graph1.clade.get(&v1).unwrap();

        //println!("clade u1 {:?}", clade_u1);
        //println!("clade v1 {:?}", clade_v1);
        let id_u1 = clade_id.get(clade_u1).unwrap();
        let id_v1 = clade_id.get(clade_v1).unwrap();

        let w1 = graph1.weight.get(&(u1,v1)).unwrap();

        weight1.insert((*id_u1,*id_v1), *w1);
        transfer_ids.insert((*id_u1,*id_v1));
    }

    for (u2,v2) in graph2.list_transfers() {
        let clade_u2  = graph2.clade.get(&u2).unwrap();
        let clade_v2  = graph2.clade.get(&v2).unwrap();

        let id_u2 = clade_id.get(clade_u2).unwrap();
        let id_v2 = clade_id.get(clade_v2).unwrap();

        let w2 = graph2.weight.get(&(u2,v2)).unwrap();

        weight2.insert((*id_u2,*id_v2), *w2);
        transfer_ids.insert((*id_u2,*id_v2));
    }
    
    for (id1,id2) in transfer_ids {
        let mut diff : f64 = 0f64;
    
        if let Some(w) =  weight1.get(&(id1,id2)) {
            diff += w;
        }
        if let Some(w) =  weight2.get(&(id1,id2)) {
            diff -= w;
        }

        distance += diff.abs();
    }

    return distance;


}

pub fn transfer_edition_distance_weighted_rust(network1 : Vec<String>, network2 : Vec<String>) -> f64 {
    let mut graph1 : Graph = parse_graph_weighted(network1);
    let mut graph2 : Graph = parse_graph_weighted(network2);

    let mut distance : f64 = 0f64;

    // Start of block ensuring same base tree
    let clades1 : Vec<Vec<usize>> = graph1.list_clades();
    for clade1 in &clades1 {
        if !graph2.has_clade(clade1) {
            let cost : f64 = graph1.remove_clade(clade1);
            distance += cost;
        }
    }

    let clades2 : Vec<Vec<usize>> = graph2.list_clades();
    for clade2 in &clades2 {
        if !graph1.has_clade(clade2) {
            let cost : f64 = graph2.remove_clade(clade2);
            distance += cost;
        }
    }

    graph1.remove_degree_2_nodes();
    graph2.remove_degree_2_nodes();
    // end of block ensuring same base tree
    
    // preprocessing rule: if there exists a clade_a -> clade_b
    // transfer in graph1 but not in graph2, remove it.
    for (u,v) in graph1.list_transfers() {
        let clade_a1 = graph1.clade.get(&u).unwrap();
        let clade_b1 = graph1.clade.get(&v).unwrap();

        let mut found_it : bool = false;

        for (w,x) in graph2.list_transfers() {
            let clade_a2 = graph2.clade.get(&w).unwrap();
            let clade_b2 = graph2.clade.get(&x).unwrap();
            
            if same_clade(&clade_a1, &clade_a2) && same_clade(&clade_b1, &clade_b2) {
                found_it = true;
                break
            }
        }
        if !found_it {
            graph1.remove_transfer(u,v);
            distance += graph1.weight.get(&(u,v)).unwrap();
        }
        
    }
    
    for (u,v) in graph2.list_transfers() {
        let clade_a2 = graph2.clade.get(&u).unwrap();
        let clade_b2 = graph2.clade.get(&v).unwrap();

        let mut found_it : bool = false;

        for (w,x) in graph1.list_transfers() {
            let clade_a1 = graph1.clade.get(&w).unwrap();
            let clade_b1 = graph1.clade.get(&x).unwrap();
            
            if same_clade(&clade_a1, &clade_a2) && same_clade(&clade_b1, &clade_b2) {
                found_it = true;
                break
            }
        }
        if !found_it {
            graph2.remove_transfer(u,v);
            distance += graph2.weight.get(&(u,v)).unwrap();
        }
    }

    graph1.remove_degree_2_nodes();
    graph2.remove_degree_2_nodes();
    // end preprocessing
    
    let mut best_score : f64 = f64::MAX;

    for v1 in powerset(&graph1.list_transfers()) {
        for v2 in powerset(&graph2.list_transfers()) {
            let graph1p : Graph = graph1.remove_transfer_set(&v1);
            let graph2p : Graph = graph2.remove_transfer_set(&v2);
            let mut weight : f64 = 0f64;
            for (u,v) in &v1 {
                weight += graph1.weight.get(&(*u,*v)).unwrap();
            }
            for (u,v) in &v2 {
                weight += graph2.weight.get(&(*u,*v)).unwrap();
            }
            if graph1p.is_iso(graph2p) {
                if weight < best_score {
                    best_score = weight;
                }
            }
        }
    }

    return distance + best_score;
}

/// Given two LGT networks given as lists of edges, computes the transfer edition distance
///
/// This computes the unweighted transfer distance, between two fully explicit
/// LGT networks (see other variants of this function, namely transfer_edition_distance_weighted
/// and transfer_edition_distance_unordered, for these cases)
///
/// the weighted (but ordered) version is a separate function because it prevents from using
/// one of the optimizations used here, namely the iteration over the "deletion sets" ordered
/// by size. Indeed, in the unweighted version, one can just iterate over the deletion
/// sets ordered by size, and stop as soon as a valid deletion set (i.e. yielding two
/// isomorphic networks) is found. 
///
/// Example of input: vec!["1 2 tree","2 3 tree","1 4 tree","4 5 tree","2 4 transfer"], {another
/// vec}
pub fn transfer_edition_distance_rust(network1 : Vec<String>, network2 : Vec<String>) -> usize {
    let mut graph1 : Graph = parse_graph(network1);
    let mut graph2 : Graph = parse_graph(network2);

    let mut distance : usize = 0;

    // Start of block ensuring same base tree
    let clades1 : Vec<Vec<usize>> = graph1.list_clades();
    for clade1 in &clades1 {
        if !graph2.has_clade(clade1) {
            let cost : usize = graph1.remove_clade(clade1) as usize;
            distance += cost;
        }
    }

    let clades2 : Vec<Vec<usize>> = graph2.list_clades();
    for clade2 in &clades2 {
        if !graph1.has_clade(clade2) {
            let cost : usize = graph2.remove_clade(clade2) as usize;
            distance += cost;
        }
    }

    graph1.remove_degree_2_nodes();
    graph2.remove_degree_2_nodes();
    // end of block ensuring same base tree

    // preprocessing rule: if there exists a clade_a -> clade_b
    // transfer in graph1 but not in graph2, remove it.
    for (u,v) in graph1.list_transfers() {
        let clade_a1 = graph1.clade.get(&u).unwrap();
        let clade_b1 = graph1.clade.get(&v).unwrap();

        let mut found_it : bool = false;

        for (w,x) in graph2.list_transfers() {
            let clade_a2 = graph2.clade.get(&w).unwrap();
            let clade_b2 = graph2.clade.get(&x).unwrap();
            
            if same_clade(&clade_a1, &clade_a2) && same_clade(&clade_b1, &clade_b2) {
                found_it = true;
                break
            }
        }
        if !found_it {
            graph1.remove_transfer(u,v);
            distance += 1;
        }
        
    }
    
    for (u,v) in graph2.list_transfers() {
        let clade_a2 = graph2.clade.get(&u).unwrap();
        let clade_b2 = graph2.clade.get(&v).unwrap();

        let mut found_it : bool = false;

        for (w,x) in graph1.list_transfers() {
            let clade_a1 = graph1.clade.get(&w).unwrap();
            let clade_b1 = graph1.clade.get(&x).unwrap();
            
            if same_clade(&clade_a1, &clade_a2) && same_clade(&clade_b1, &clade_b2) {
                found_it = true;
                break
            }
        }
        if !found_it {
            graph2.remove_transfer(u,v);
            distance += 1;
        }
    }

    graph1.remove_degree_2_nodes();
    graph2.remove_degree_2_nodes();
    // end preprocessing

    let transfers1 : Vec<(usize,usize)> = graph1.list_transfers(); 
    let transfers2 : Vec<(usize,usize)> = graph2.list_transfers(); 
    
    let mut found_it : bool = false;


    for size_deletion_set in 0..=(transfers1.len()+transfers2.len()) {
        for x in all_integers_with_weight_k((transfers1.len()+transfers2.len()).try_into().unwrap(), size_deletion_set.try_into().unwrap()) {
            let deleted_transfers1 : Vec<&(usize,usize)> = transfers1.iter()
                .enumerate()
                .filter(|&(t,_)| (x >> t) % 2 == 1)
                .map(|(_, element)| element)
                .collect(); 
            
            let deleted_transfers2 : Vec<&(usize,usize)> = transfers2.iter()
                .enumerate()
                .filter(|&(t,_)| (x >> (transfers1.len()+t)) % 2 == 1)
                .map(|(_, element)| element)
                .collect(); 

            let graph1p : Graph = graph1.remove_transfer_set(&deleted_transfers1);
            let graph2p : Graph = graph2.remove_transfer_set(&deleted_transfers2);
            if graph1p.is_iso(graph2p) {
                found_it = true;
                //println!("found it !");
                distance += size_deletion_set;
                break
            }
        }
        if found_it {
            break
        }
    }
    assert!(found_it);

    return distance;
}

pub fn transfer_edition_distance_unordered_rust(network1 : Vec<String>, network2 : Vec<String>) -> usize {

    let mut graph1 : Graph = parse_graph(network1);
    let mut graph2 : Graph = parse_graph(network2);
    
    let mut distance : usize = 0;

    // Start of block ensuring same base tree
    let clades1 : Vec<Vec<usize>> = graph1.list_clades();
    for clade1 in &clades1 {
        if !graph2.has_clade(clade1) {
            let cost : usize = graph1.remove_clade(clade1) as usize;
            distance += cost;
        }
    }

    let clades2 : Vec<Vec<usize>> = graph2.list_clades();
    for clade2 in &clades2 {
        if !graph1.has_clade(clade2) {
            let cost : usize = graph2.remove_clade(clade2) as usize;
            distance += cost;
        }
    }

    graph1.remove_degree_2_nodes();
    graph2.remove_degree_2_nodes();
    // end of block ensuring same base tree
    
    let mut intersection_size : usize = 0;

    for (u1,v1) in graph1.list_transfers() {
        let clade_u1  = graph1.clade.get(&u1).unwrap();
        let clade_v1  = graph1.clade.get(&v1).unwrap();

        let mut is_in_intersect : bool = false;

        for (u2,v2) in graph2.list_transfers() {
            let clade_u2  = graph2.clade.get(&u2).unwrap();
            let clade_v2  = graph2.clade.get(&v2).unwrap();

            if same_clade(&clade_u1, &clade_u2) && same_clade(&clade_v1, &clade_v2) {
                is_in_intersect = true;
                break;
            }
        }

        if is_in_intersect {
            intersection_size += 1;
        }
    }

    distance += graph1.list_transfers().len()+graph2.list_transfers().len()-2*intersection_size;

    return distance;
}

#[pyfunction]
fn transfer_edition_distance(network1 : Vec<String>, network2 : Vec<String>) -> PyResult<usize> {
    let distance : usize = transfer_edition_distance_rust(network1, network2);
    return Ok(distance);
}

#[pyfunction]
fn transfer_edition_distance_weighted(network1 : Vec<String>, network2 : Vec<String>) -> PyResult<f64> {
    let distance : f64 = transfer_edition_distance_weighted_rust(network1, network2);
    return Ok(distance);
}

#[pyfunction]
fn transfer_edition_distance_unordered(network1 : Vec<String>, network2 : Vec<String>) -> PyResult<usize> {
    let distance : usize = transfer_edition_distance_unordered_rust(network1, network2);
    return Ok(distance);
}

#[pyfunction]
fn transfer_edition_distance_unordered_weighted(network1 : Vec<String>, network2 : Vec<String>) -> PyResult<f64> {
    let distance : f64 = transfer_edition_distance_unordered_weighted_rust(network1, network2);
    return Ok(distance);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ted() {
        let network1 = vec!["1 8 tree",
                            "1 7 tree",
                            "8 6 tree",
                            "7 3 tree",
                            "6 2 tree",
                            "2 4 tree",
                            "2 9 tree",
                            "9 5 tree",
                            "6 7 transfer",
                            "8 9 transfer"];
 
        let network2 = vec!["1 6 tree",
                            "1 7 tree",
                            "6 8 tree",
                            "7 3 tree",
                            "8 2 tree",
                            "2 4 tree",
                            "2 9 tree",
                            "9 5 tree",
                            "6 7 transfer",
                            "8 9 transfer"];

        let d_ordered = transfer_edition_distance_rust(network1.into_iter().map(|x| x.to_string()).collect(), 
                                                       network2.into_iter().map(|x| x.to_string()).collect());

        assert_eq!(d_ordered,2);        
    }

    #[test]
    fn test_ted_unordered() {
        let network1 = vec!["1 8 tree",
                            "1 7 tree",
                            "8 6 tree",
                            "7 3 tree",
                            "6 2 tree",
                            "2 4 tree",
                            "2 9 tree",
                            "9 5 tree",
                            "6 7 transfer",
                            "8 9 transfer"];
 
        let network2 = vec!["1 6 tree",
                            "1 7 tree",
                            "6 8 tree",
                            "7 3 tree",
                            "8 2 tree",
                            "2 4 tree",
                            "2 9 tree",
                            "9 5 tree",
                            "6 7 transfer",
                            "8 9 transfer"];

        let d_unordered = transfer_edition_distance_unordered_rust(network1.clone().into_iter().map(|x| x.to_string()).collect(), 
                                                         network2.clone().into_iter().map(|x| x.to_string()).collect());
        assert_eq!(d_unordered,0);        
    }

    #[test]
    fn test_to_string() {
        let cano_label : CanonicalLabel = CanonicalLabel {clade : vec![1,2,3], rank : 8};
        assert_eq!(cano_label.to_string(),"123-8".to_string());
    }

    #[test]
    fn test_powerset() {
        let vec : Vec<(usize, usize)> = vec![(0,1),(1,2)];
        let subsets : Vec<Vec<&(usize,usize)>> = powerset(&vec); 
        let result_vec: Vec<Vec<(usize, usize)>> = vec![vec![], vec![(0,1)], vec![(1,2)], vec![(0,1),(1,2)]];
        //println!("{:?}", subsets);
        //println!("{:?}", result_vec);
        for k in 0..result_vec.len() {
            let subset : Vec<(usize,usize)> = result_vec[k].clone();
            let subset2 : Vec<&(usize, usize)> = subsets[k].clone();
            assert_eq!(subset.len(),subset2.len());
            for l in 0..subset.len() {
                let (u1,v1) : (usize,usize) = subset[l];
                let &(u2,v2) : &(usize,usize) = subset2[l];
                assert_eq!(u1,u2);
                assert_eq!(v1,v2);
            }
        }
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
fn dlgt_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(transfer_edition_distance,m)?)?;
    m.add_function(wrap_pyfunction!(transfer_edition_distance_weighted,m)?)?;
    m.add_function(wrap_pyfunction!(transfer_edition_distance_unordered,m)?)?;
    m.add_function(wrap_pyfunction!(transfer_edition_distance_unordered_weighted,m)?)?;
    Ok(())
}

