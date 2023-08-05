import { Component, OnInit, Input, OnChanges, SimpleChanges, Output,EventEmitter } from '@angular/core';
import { ITC } from '@app/_interfaces/ITC'; 
import { IEnv } from '@app/_interfaces/IEnv';
import { IApp } from '@app/_interfaces/IApp';
import { IAction } from '@app/_interfaces/IAction';
import { TcService } from '@app/_services/tc.service';

@Component({
  selector: 'app-tcaction',
  templateUrl: './tcaction.component.html',
  styleUrls: ['./tcaction.component.css']
})
export class TcactionComponent implements OnInit, OnChanges  {
  @Input() refreshApps : boolean;
  @Input() curr_tc : ITC;
  @Input() env:IEnv;
  @Output() actionKey = new EventEmitter<IAction>();

  apps : IApp[];
  act :IAction = { action:'',type:'TC',id:0,name:''}
  session:any;
  logsize:number;

  constructor(
    private tcService : TcService
    ) { }

  ngOnInit(): void {
//    this.tcService.getApps(this.curr_tc.id).subscribe(
//      data => this.apps = data)
    this.tcService.getApps(this.curr_tc.id).subscribe(
      data => this.apps = data.filter( a => a.status !== ""))

    this.tcService.getSession().subscribe(
      data => this.session = data
    )
    this.tcService.getInfo(this.curr_tc.id,'tc_logsize').subscribe(
      data => this.logsize= data.logsize
    )
  }

  ngOnChanges(changes: SimpleChanges) {
    this.tcService.getApps(this.curr_tc.id).subscribe(
      data => this.apps = data.filter( a => a.status !== ""))

    this.tcService.getInfo(this.curr_tc.id,'tc_logsize').subscribe(
      data => this.logsize= data.logsize
      )
  }  

  selectStart(tc:ITC) {
    this.act.action = "START"
    this.act.id=tc.id
    this.act.name = `${ tc.name } on ${ this.env.name }`
    if (this.session.ldap_authorized <= this.env.authlvl) {
      this.actionKey.emit(this.act)
    }  
  }

  selectKill(tc:ITC) {
    this.act.action = "KILL"
    this.act.id=tc.id
    this.act.name = `${ tc.name } on ${ this.env.name }`
    if (this.session.ldap_authorized <= this.env.authlvl) {
      this.actionKey.emit(this.act)
    }  
  }

  selectStop(tc:ITC) {
    this.act.action = "STOP"
    this.act.id=tc.id
    this.act.name = `${ tc.name } on ${ this.env.name }`
    if (this.session.ldap_authorized <= this.env.authlvl) {
      this.actionKey.emit(this.act)
    }  
  }

  newAction(act:IAction) {
    if (this.session.ldap_authorized <= this.env.authlvl) {
      this.actionKey.emit(act)
    }  
  }

}
