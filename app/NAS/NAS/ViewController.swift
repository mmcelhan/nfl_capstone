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
        let vc = SFSafariViewController(url:URL(string:"https://ischool.berkeley.edu/~andrew.morris/class/w210/stub_site/draft_rank.html")!)
        vc.preferredBarTintColor = UIColor .black
        
        present(vc, animated: true)
    }
    @IBAction func candidate_tapped(){
        let vc = SFSafariViewController(url:URL(string:"https://ischool.berkeley.edu/~andrew.morris/class/w210/stub_site/candidate.html")!)
        vc.preferredBarTintColor = UIColor .black
        present(vc, animated: true)
    }
    
    @IBAction func criteria_tapped(){
        let vc = SFSafariViewController(url:URL(string:"https://ischool.berkeley.edu/~andrew.morris/class/w210/stub_site/criteria.html")!)
        vc.preferredBarTintColor = UIColor .black
        present(vc, animated: true)
    }
    @IBAction func comprank_tapped(){
        let vc = SFSafariViewController(url:URL(string:"https://ischool.berkeley.edu/~andrew.morris/class/w210/stub_site/comp_rank.html")!)
        vc.preferredBarTintColor = UIColor .black
        present(vc, animated: true)
    }
}
