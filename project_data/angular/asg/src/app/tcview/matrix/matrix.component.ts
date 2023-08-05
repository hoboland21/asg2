import { Component, OnInit, OnChanges, SimpleChanges, Output, EventEmitter, Input } from '@angular/core';
import { ITC } from '@app/_interfaces/ITC'; 
import { IEnv } from '@app/_interfaces/IEnv'; 
import { IAction } from '@app/_interfaces/IAction'; 
import { TcService } from '@app/_services/tc.service';
@Component({
  selector: 'app-matrix',
  styleUrls: ['./matrix.component.css'],
  template: ` 
   <div *ngFor="let e of eList">
    <app-enview [curr_tc]='curr_tc' [env] = 'e' 
      (newTCSelect)='tcSelector($event)' 
      (newEnvSelect)='envSelector($event)' 
      > </app-enview>
  </div>
`

})
export class MatrixComponent implements OnInit,OnChanges {

  eList : IEnv[];
  selected : string;
  now_env : IEnv;
  curr_tc : ITC;
  curr_env: IEnv;
 
  @Output() emitMtx = new EventEmitter<any>();
  @Input()  flag:boolean ;

  constructor(
    private tcService : TcService


  ) { }

  ngOnInit(): void {
    this.tcService.getEnvList().subscribe(
      data => this.eList = data
    )
  }
  ngOnChanges(changes:SimpleChanges) {
    this.tcService.getEnvList().subscribe(
      data => this.eList = data
    )
 
  }


 //-----------------------
 tcSelector(tc:ITC) {
  //-----------------------
    this.curr_tc = tc
    this.selected = "TC"
    const act:IAction = {type:"CMD",id:tc.id,action:"TCREFRESH"}
    this.tcService.postTCmd(act).subscribe(
      d1 => {
        this.tcService.getEnvList().subscribe(
          data => this.eList = data
        );
        this.tcService.getEnv(tc.env).subscribe(
          data => {
            this.now_env = data
            this.emitMtx.emit({selected:'TC',tc:tc,env:data})
          }
        )
      }    
    )
    
  }
  //-----------------------
  envSelector(env:IEnv) {
    //-----------------------
    this.curr_env = env
      this.selected = "Env"
      this.emitMtx.emit({selected:'Env',env:env})
    }


}
