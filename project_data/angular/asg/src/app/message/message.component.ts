import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { IAction } from '@app/_interfaces/IAction';
import { ILog } from '@app/_interfaces/ILog';
import { LoggingService } from '@app/_services/logging.service';
import { TcService }  from '@app/_services/tc.service'
import { AuthService } from '@app/_services/auth.service';
import { Subscription } from 'rxjs';
import { map,concatMap, tap  } from 'rxjs/operators';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit,OnChanges {
  transmitAction = []
  @Input() newItem:IAction;
  log:ILog 
  display:any = []
  subscription : Subscription;
  isLoggedIn: boolean;
  data:any;
  log_count = 100
  username:string =""


  constructor(
    private loggingService: LoggingService,
    private authService: AuthService,
    private tcService:TcService
  ) { }

  UserCheck$ = this.authService.isLoggedIn.pipe(
      concatMap((session) => this.tcService.getSession()
      )
    )
  
  ngOnInit(): void {
    this.loggingService.getLogs(this.log_count).subscribe(
      (data) => {
        this.display = data
      }
    )

}

  createLog(username:string,log_count:number) {
    this.log = {name:'',type:'',action:'',status:'',label:'',username:username } 
    if (this.newItem.name) { this.log.name = this.newItem.name; }
    if (this.newItem.type) {  this.log.type = this.newItem.type;}
    if (this.newItem.action)  { this.log.action = this.newItem.action;}
    if (this.newItem.status) {  this.log.status = this.newItem.status;}
    if (this.newItem.label)  { this.log.label = this.newItem.label;}
    this.log.time = new Date().toLocaleString('en-US', { timeZone: 'PST' })

    this.UserCheck$.pipe(
      tap((auth ) => {
        this.log.username = auth.user
      } ),
     concatMap((auth) => this.loggingService.postLog(this.log,log_count).pipe(
      map(
        data => this.display = data.loglist
      )))).subscribe()
   }


  
  ngOnChanges(changes: SimpleChanges){
    this.createLog(this.username,this.log_count)
    
    /*
    this.transmitAction.push(this.newItem)
    
    this.display = []
    this.transmitAction.forEach( data => { 
        this.display.push(data) ;
      });
    this.display.reverse()
  
*/  
  }
}
