//
//  ViewController.swift
//  NAS
//
//  Created by Andrew Morris on 6/6/20.
//  Copyright © 2020 MIDS Capstone 2020. All rights reserved.
//

import UIKit
import SafariServices

class ViewController: UIViewController{
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func draftrank_tapped(){
        let vc = SFSafariViewController(url:URL(string:"https://groups.ischool.berkeley.edu/NFL-Auto-Scout/draft_rank.html")!)
        vc.preferredBarTintColor = UIColor .black
        
        present(vc, animated: true)
    }
    @IBAction func candidate_tapped(){
        let vc = SFSafariViewController(url:URL(string:"https://groups.ischool.berkeley.edu/NFL-Auto-Scout/candidate.html")!)
        vc.preferredBarTintColor = UIColor .black
        present(vc, animated: true)
    }
    
    @IBAction func criteria_tapped(){
        let vc = SFSafariViewController(url:URL(string:"https://groups.ischool.berkeley.edu/NFL-Auto-Scout/criteria.html")!)
        vc.preferredBarTintColor = UIColor .black
        present(vc, animated: true)
    }
    @IBAction func comprank_tapped(){
        let vc = SFSafariViewController(url:URL(string:"https://groups.ischool.berkeley.edu/NFL-Auto-Scout/comp_rank.html")!)
        vc.preferredBarTintColor = UIColor .black
        present(vc, animated: true)
    }
}
