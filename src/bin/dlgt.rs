//! Comments in main.rs
//! 
use std::fs::read_to_string;
use dlgt_module::transfer_edition_distance_rust; 
use dlgt_module::transfer_edition_distance_unordered_rust; 
use dlgt_module::transfer_edition_distance_weighted_rust; 
use dlgt_module::transfer_edition_distance_unordered_weighted_rust; 

use clap::Parser;

#[derive(Parser)]
struct Cli {
    fname1 : String,
    fname2 : String,
    #[arg(short, long)]
    unordered: bool,
    #[arg(short, long)]
    weighted: bool
}

fn main() {
    let cli = Cli::parse();
    //println!("{:?} {:?}", cli.fname1, cli.fname2);
    let mut lines1 : Vec<String> = read_to_string(cli.fname1).unwrap().lines().map(String::from).collect();
    let mut lines2 : Vec<String> = read_to_string(cli.fname2).unwrap().lines().map(String::from).collect();

    lines1.remove(0);
    lines2.remove(0);

    if cli.weighted {
        let d64 : f64;
        if cli.unordered {
            d64 = transfer_edition_distance_unordered_weighted_rust(lines1, lines2);
        }
        else {
            d64 = transfer_edition_distance_weighted_rust(lines1, lines2);
        }
        println!("the distance is {:?} (unordered: {:?}, weighted: {:?})", d64 , cli.unordered, cli.weighted);
    }
    else {
        let d: usize;
        if cli.unordered {
            d = transfer_edition_distance_unordered_rust(lines1, lines2);
        }
        else {
            d = transfer_edition_distance_rust(lines1, lines2);
        }
        println!("the distance is {:?} (unordered: {:?}, weighted: {:?})", d , cli.unordered, cli.weighted);
    }

}
