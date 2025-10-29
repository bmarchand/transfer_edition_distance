use std::fs::read_to_string;
use ted_module::transfer_edition_distance_rust; 
use ted_module::transfer_edition_distance_unordered_rust; 

use clap::Parser;

#[derive(Parser)]
struct Cli {
    fname1 : String,
    fname2 : String,
    #[arg(short, long)]
    unordered: bool
}

fn main() {
//    let fname1 = std::env::args().nth(1).expect("no fname1 given");
//    let fname2 = std::env::args().nth(2).expect("no fname2 given");
    let cli = Cli::parse();

    let mut lines1 : Vec<String> = read_to_string(cli.fname1).unwrap().lines().map(String::from).collect();
    let mut lines2 : Vec<String> = read_to_string(cli.fname2).unwrap().lines().map(String::from).collect();

    lines1.remove(0);
    lines2.remove(0);

    let mut d: usize = 0;
    if cli.unordered {
        d = transfer_edition_distance_unordered_rust(lines1, lines2);
    }
    else {
        d = transfer_edition_distance_rust(lines1, lines2);
    }

    println!("the distance is {:?} (unordered: {:?})", d ,cli.unordered);
}
