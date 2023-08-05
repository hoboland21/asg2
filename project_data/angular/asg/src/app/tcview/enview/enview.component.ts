import { Component, Input, OnInit } from '@angular/core';
import { ITC } from '@app/_interfaces/ITC'; 
import { IEnv } from '@app/_interfaces/IEnv'; 
import { TcService } from '@app/_services/tc.service';
import { ControlContainer } from '@angular/forms';
import { Output, EventEmitter } from '@angular/core';
@Component({
  selector: 'app-enview',
  templateUrl: './enview.component.html',
  styleUrls: ['./enview.component.css']
})
export class EnviewComponent implements OnInit {
  @Input() env : IEnv
  @Input() curr_tc : ITC 
  @Output() newTCSelect = new EventEmitter<ITC>();
  @Output() newEnvSelect = new EventEmitter<IEnv>();
  
  tcList : ITC[]
  constructor(
    private tcService : TcService,
  ) { }

  selectTC(tc_select:ITC) {
    this.newTCSelect.emit(tc_select)
    this.curr_tc = tc_select;
  }

  
  selectEnv(env_select:IEnv) {
    this.newEnvSelect.emit(env_select)
  }

  ngOnInit(): void {
     if( !this.curr_tc ) {
      this.curr_tc = {} as ITC
     }
     this.tcService.getTCList(this.env.id).subscribe(
      data => { 
        this.tcList = data
      }
    )
  }
}
