import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { ITC } from '@app/_interfaces/ITC';
import { IEnv } from '@app/_interfaces/IEnv';
import { IAction } from '@app/_interfaces/IAction';
import { TcService } from '@app/_services/tc.service';

@Component({
  selector: 'app-envaction',
  templateUrl: './envaction.component.html',
  styleUrls: ['./envaction.component.css']
})
export class EnvactionComponent implements OnInit, OnChanges {
  @Input() curr_env: IEnv
  @Output() actionKey = new EventEmitter<IAction>();

  session: any;
  loglist : []
  instinfo: []
  act: IAction = { action: '', type: 'Env', id: 0, name: '' }
  envstatus: boolean;

  constructor(
    private tcService: TcService
  ) { }

  selectStart(env: IEnv) {
    this.act.action = "START"
    this.act.id = env.id
    this.act.name = `All TC instances on ${env.name} `
    if (this.session.ldap_authorized <= env.authlvl) {
      this.actionKey.emit(this.act)
    }
  }
  selectStop(env: IEnv) {
    this.act.action = "STOP"
    this.act.id = env.id
    this.act.name = `All TC instances on ${env.name} `
    if (this.session.ldap_authorized <= env.authlvl) {
      this.actionKey.emit(this.act)
    }
  }


  getLogfiles(env:IEnv) {
    this.loglist =[]
    this.tcService.getInfo(env.id,"env_logsize").subscribe(
      data => {
        this.loglist=data
      }
    )
  }
  ngOnChanges(changes:SimpleChanges) {

    this.getLogfiles(this.curr_env)

  }
  ngOnInit(): void {
    this.tcService.getSession().subscribe(
      data => this.session = data
    )
    this.tcService.getEnvStatus(this.curr_env).subscribe(
      data => this.envstatus = data.env_status
    )
    this.getLogfiles(this.curr_env)
  }



}
