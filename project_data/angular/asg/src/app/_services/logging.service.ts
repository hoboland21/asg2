import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map,concatMap  } from 'rxjs/operators';
import { ILog } from '@app/_interfaces/ILog';
import { IUser } from '@app/_interfaces/IUser';
import { AppEnv } from '@app/_helpers/appenv';


const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class LoggingService {
  constructor(
    private router: Router, 
    private http: HttpClient ,
    private env: AppEnv) { }

  private API = this.env.WEB_API

  public getLogs(count:number): Observable<ILog[]> {
    return this.http.get<any[]>(`${this.API}/listlogs/${count}/`,httpOptions) 
  }

  public postLog(log:ILog,count:number): Observable<any> {
    return this.http.post<any>(`${this.API}/postlog/`,log,httpOptions).pipe( 
      concatMap((newlog) => this.getLogs(count).pipe(
        map(loglist => {
          console.log(loglist,newlog)
          return { loglist, newlog }
          })
        )
      )
    )
  }
}