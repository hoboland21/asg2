import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import {  FormGroup, FormControl } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { take } from 'rxjs/operators';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  formdata;

  constructor(
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router,
    ) { }

  ngOnInit(): void {
    
    this.formdata = new FormGroup({
      username: new FormControl(''),
      password: new FormControl('')

    });
  }

  onSubmit(data) {
    this.authService.login(data)
      .subscribe(
         (data) => {
          localStorage.setItem('token',data.token);
          this.authService.changeLoggedIn(true);
          this.router.navigate(['desktop']);

        
      })
    }
  } 
  


  

