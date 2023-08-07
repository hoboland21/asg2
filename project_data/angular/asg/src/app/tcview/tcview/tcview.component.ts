import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { ITC } from '@app/_interfaces/ITC'; 
import { IEnv } from '@app/_interfaces/IEnv'; 
import { IAction } from '@app/_interfaces/IAction'; 

import { TcService } from '@app/_services/tc.service';

@Component({
  selector: 'app-tcview',
  templateUrl: './tcview.component.html',
  styleUrls: ['./tcview.component.css']
})
export class TcviewComponent implements OnInit {

  eList : IEnv[];
  x;
  curr_tc : ITC;
  curr_env: IEnv;
  selected : string;
  now_env : IEnv;
  actionCode : IAction;
  actionVar:IAction;
  refreshing:boolean;
  autoRefresh:boolean;
  config_switch:boolean = false
  newItem;
  refreshFlag:boolean
   
  constructor(
    private tcService : TcService
  ) 
  
  { }

  //-----------------------
  ngOnInit(): void {
  //-----------------------
  this.autoRefreshOff();
  this.refreshCmd();

  }
  //-----------------------
  ngOnDestroy() {
  //-----------------------
    if (this.x) {
          clearInterval(this.x)
        }
      }


  //-----------------------
  mtxEmit(mtx) {
  //-----------------------
    this.selected = mtx.selected
    if (mtx.selected == "TC") {
      
      this.curr_tc = mtx.tc
      this.now_env = mtx.env
    }
    else if(mtx.selected == "Env") {
      this.curr_env = mtx.env
    }
  }



  //-----------------------
  autoRefreshOn() {
  //-----------------------
    this.refreshCmd();
        this.x = setInterval(()=> { this.refreshCmd(); },60000);
        this.autoRefresh = true;  
      }
  //-----------------------
  autoRefreshOff() {
  //-----------------------
    if (this.x) {
          clearInterval(this.x)
        }
        this.autoRefresh = false;
      }
 
  //-----------------------
  message(msg:any) {
  //-----------------------
    this.newItem = msg
  }
 
  //-----------------------
  refreshCmd() {
  //-----------------------
    this.actionVar = { type:'CMD',action:"REFRESH",id:0 , name:''};
    this.refreshing = true
    this.tcService.postTCmd(this.actionVar)
    .subscribe( 
      data =>  {
            
   //         data.status = "CMD Complete"
   //         this.message(data);
            this.refreshing = false
            this.refreshFlag = !this.refreshFlag
        }
    )
//    this.actionVar.status = "CMD Sent"
//    this.message(this.actionVar)
  }

  //-----------------------
  actionSelector(act:IAction) {
  //-----------------------
    this.actionCode = act
  //    this.actionKey.emit(act)
    }
//-----------------------
  actionConfirm(act:IAction) {
//-----------------------
    this.tcService.postTCmd(act)
      .subscribe( 
        data =>  {
          data.status = "CMD Rcvd"
          this.message(data);
//          this.refreshCmd();
        },
        error =>  {
          error.status = "Error"
          this.message(error)
        }

      )
    // send off to the api for action
    act.status = "CMD Sent"    
    this.message(act)
    this.actionCode = null
  }
  //-----------------------
  actionCancel() {
  //-----------------------
    this.actionCode = null
    
  }




}


