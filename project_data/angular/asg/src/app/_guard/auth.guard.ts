import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router, UrlTree } from '@angular/router';
import { AuthService } from '@app/_services/auth.service';
import { Observable,Subscription } from 'rxjs';
import { authInterceptorProviders } from '@app/_helpers/auth.interceptor';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor( 
    private authService: AuthService
  ) {}


  

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot):  Observable<boolean> {
      return this.authService.isLoggedIn
      }
  
}
