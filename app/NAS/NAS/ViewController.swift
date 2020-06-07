//
//  ViewController.swift
//  NAS
//
//  Created by Andrew Morris on 6/6/20.
//  Copyright © 2020 MIDS Capstone 2020. All rights reserved.
//

import UIKit
import WebKit

class ViewController: UIViewController {
    @IBOutlet weak var webView:WKWebView?
    
    override func viewDidLoad()
    {
        super.viewDidLoad()

        let request = URLRequest(url: URL(string: "https://learnappmaking.com")!)

        webView?.load(request)
    }
}
