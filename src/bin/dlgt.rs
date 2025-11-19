//! Comments in main.rs
//! 
use std::fs::read_to_string;
use dlgt_module::transfer_edition_distance_rust; 
use dlgt_module::transfer_edition_distance_unordered_rust; 
use dlgt_module::transfer_edition_distance_weighted_rust; 
use dlgt_module::transfer_edition_distance_unordered_weighted_rust; 

use clap::Parser;

/// A command-line tool for computing transfer edition distances between LGT networks.
#[derive(Parser)]
struct Cli {
    /// filename for network1 (.gr format)
    fname1 : String,
    /// filename for network2 (.gr format)
    fname2 : String,
    /// Whether to use the unordered distance or not (default: ordered)
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
