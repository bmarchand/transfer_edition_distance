use std::fs::read_to_string;
use ted_module::transfer_edition_distance_rust; 

fn main() {
    let fname1 = std::env::args().nth(1).expect("no fname1 given");
    let fname2 = std::env::args().nth(2).expect("no fname2 given");

    let mut lines1 : Vec<String> = read_to_string(fname1).unwrap().lines().map(String::from).collect();
    let mut lines2 : Vec<String> = read_to_string(fname2).unwrap().lines().map(String::from).collect();

    lines1.remove(0);
    lines2.remove(0);

    let d : usize = transfer_edition_distance_rust(lines1, lines2);

    println!("the distance is {:?}", d);
}
