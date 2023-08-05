import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map  } from 'rxjs/operators';
import { AppEnv } from '@app/_helpers/appenv';
import { ITC } from '@app/_interfaces/ITC'; 
import { IEnv } from '@app/_interfaces/IEnv'; 
import { IApp } from '@app/_interfaces/IApp'; 
import { IAction } from '@app/_interfaces/IAction'; 

import { AuthService } from '@app/_services/auth.service'

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
}; 

const httpAuthOptions = {
  headers: new HttpHeaders({ 
      'Content-Type': 'application/json' ,
      "Authorization": "Basic " + btoa('quasar:pimil210') 
  })
};

const nrHttpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json',
    'X-Api-Key' : '{a1f4b78c17f0699a1566c786540236312129abe51783eda}',
    'Accept' : 'application/json'
    })
};

@Injectable({
  providedIn: 'root'
})
export class TcService {
  envList: IEnv[];
  TClist = [] ;

  constructor(   private router: Router, 
    private http: HttpClient ,
    private env: AppEnv,
    private authService: AuthService ) 
    
    {  }

  private API = this.env.WEB_API


  public getEnvList(): Observable<IEnv[]> {
    return this.http.get<any>(`${this.API}/envlist/`,httpOptions) 
  }

  public getEnvStatus(env:IEnv) : Observable<any>{
    return this.http.get<any>(`${this.API}/envstatus/${env.id}/`,httpOptions)
  }

  public getTCList(env:number): Observable<ITC[]> {
    return this.http.get<any>(`${this.API}/tclist/${env}/`,httpOptions) 
  }
  public getEnv(envid:number): Observable<IEnv> {
    return this.http.get<any>(`${this.API}/env/${envid}/`,httpOptions) 
  }

  public getApps(tcid:number): Observable<IApp[]> {
    return this.http.get<any>(`${this.API}/app/${tcid}/`,httpOptions) 
  }

  public postTCmd(cmd:IAction): Observable<any> {
    console.log(cmd)
    return this.http.post<any>(`${this.API}/cmd/`,cmd,httpOptions)
  }

  public getNRAlerts(): Observable<any>{
    return this.http.get<any>(`${this.API}/newrelic/`,httpOptions) 
    
  }
  public getSession(): Observable<any>{
    return this.http.get<any>(`${this.API}/session/`,httpOptions) 
  }
  public Search(query:string) : Observable<any[]>{
    return this.http.get<any>(`${this.API}/appsearch/${query}/`,httpOptions) 
  }
  public getConfig(tc:ITC,fname:string) : Observable<any>{
    return this.http.get<any>(`${this.API}/config/${tc.id}/${fname}/`,httpOptions) 
  }
  public getStatus(tc:ITC) : Observable<any>{
    return this.http.get<any>(`${this.API}/status/${tc.id}/`,httpOptions) 
  }
  public getInfo(anyid:number,cmd:string) : Observable<any>{
    return this.http.get<any>(`${this.API}/info/${anyid}/${cmd}/`,httpOptions) 
  }
}






/*
    headers = {
      'X-Api-Key': 'a1f4b78c17f0699a1566c786540236312129abe51783eda',
      }
      response = requests.get('https://api.newrelic.com/v2/alerts_violations.json', headers=headers)
      
      return json.loads(response.text)["violations"]
  
*/  
