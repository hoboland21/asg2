import { Component, Input, OnInit } from '@angular/core';
import { IEnv } from '@app/_interfaces/IEnv';

import { ITC } from '@app/_interfaces/ITC';
import { TcService } from "@app/_services/tc.service"
@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent implements OnInit {
  config:any
  fname:string
  
  @Input() tc:ITC;
  @Input() env:IEnv;

  constructor(
    private tcService : TcService

  ) { }
  ngOnInit(): void {
  }


  getStatus() {
    this.tcService.getStatus(this.tc).subscribe(
      data => {
       const blob = new Blob([data.data], {type: 'application/html'})
       const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        a.download = "StatusReport.html"
        a.click()
        URL.revokeObjectURL(objectUrl)

      }
    )

  }
  getConfig(fname:string) {
    console.log("Entering get Config actionm")
     this.tcService.getConfig(this.tc,fname).subscribe(
      data => {
       const blob = new Blob([data.data], {type: 'application/text'})
       const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        a.download = fname
        a.click()
        URL.revokeObjectURL(objectUrl)

      }
    )

  }
}
