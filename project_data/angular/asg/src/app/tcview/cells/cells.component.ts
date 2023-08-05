import { Component, OnInit,Input, Output, EventEmitter  } from '@angular/core';
import { IAction } from '@app/_interfaces/IAction'
import { IApp } from '@app/_interfaces/IApp'
import { IEnv } from '@app/_interfaces/IEnv'
import { ITC } from '@app/_interfaces/ITC'
@Component({
  selector: 'app-cells',
  templateUrl: './cells.component.html',
  styleUrls: ['./cells.component.css']
})



export class CellsComponent implements OnInit {
  @Input() app : IApp
  @Input() env : IEnv
  @Input() tc  : ITC
  
  @Output() actionKey = new EventEmitter<IAction>();
  
  act : IAction = { type:'',action:'',id:0 , name:''};
  address : string;
  slice: string;
  
  constructor() { }

  selectStart(app:IApp) {
    this.act.action = "START";
    this.act.type="App";
    this.act.id = app.id
    this.act.name = `Application (${app.name})  on ${this.env.name} ${this.tc.name}  `
    this.actionKey.emit(this.act)

  }
  

  

  selectStop(app:IApp) {
    this.act.action = "STOP";
    this.act.type="App";
    this.act.id = app.id
    this.act.name = `Application (${app.name})  on ${this.env.name} ${this.tc.name}  `
    this.actionKey.emit(this.act)

  }

  
  ngOnInit(): void {
    var server  :string

    if (this.env.name.slice(-2) == '02') {
      var ss  = this.env.name.split('-')
      server = `rh-${ss[0]}-02.pdx.odshp.com`
    }
    else {
      server = `rh-${this.env.name}-01.pdx.odshp.com`
      
    }
    // Must be changed if exceeding TC10

    let port = Number(this.tc.name.substring(2,4)) + 8080


    this.address = `${server}:${port}`
   
  }

}
