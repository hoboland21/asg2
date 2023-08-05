import { Component, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { AuthService } from '@app/_services/auth.service';
import { Subscription } from 'rxjs';
import { TcService }  from '@app/_services/tc.service'
import { IAction } from '@app/_interfaces/IAction'
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  constructor(
    private authService : AuthService,
    private tcService: TcService 
    ) { }
  subscription : Subscription;
  isLoggedIn: boolean;
  username:string;
  data:any;
  request_init = false
  ngOnInit(): void {
    this.subscription = this.authService.isLoggedIn.subscribe(
      token => {
        this.isLoggedIn = token;
          this.tcService.getSession().subscribe(
            data => {
              if(token) {
                this.username = data.user;
                this.data =data
              }
              else {
                this.username = ""
              }
            }
        )
      }
    )
  }


  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

   initdb():void {
      const act:IAction = {type:"CMD",id:0,action:"INITDB"}
      
      this.tcService.postTCmd(act).subscribe(
         data => console.log(data)
      )
   }

  logout(): void {

    this.authService.logout()
  }
}
