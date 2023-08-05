import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';

import { authInterceptorProviders } from './_helpers/auth.interceptor';
import { AppEnv } from './_helpers/appenv';
import { DesktopComponent } from './desktop/desktop.component';
import { TcviewComponent } from './tcview/tcview/tcview.component';
import { EnviewComponent } from './tcview/enview/enview.component';
import { AppsearchComponent } from './tcview/appsearch/appsearch.component';
import { NrelicComponent } from './tcview/nrelic/nrelic.component';
import { ConfigComponent } from './tcview/config/config.component';
import { CellsComponent } from './tcview/cells/cells.component';
import { TcactionComponent } from './tcview/tcaction/tcaction.component';
import { EnvactionComponent } from './tcview/envaction/envaction.component';
import { MessageComponent } from './message/message.component';
import { MatrixComponent } from './tcview/matrix/matrix.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { GaugeModule } from 'angular-gauge';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatButtonModule } from "@angular/material/button" ;




@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DesktopComponent,
    TcviewComponent,
    EnviewComponent,
    AppsearchComponent,
    NrelicComponent,
    ConfigComponent,
    CellsComponent,
    TcactionComponent,
    EnvactionComponent,
    MessageComponent,
    MatrixComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule, 
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    NgbModule,

    GaugeModule.forRoot(),

    BrowserAnimationsModule,
    MatButtonModule
  ],
  providers: [authInterceptorProviders, AppEnv],
  bootstrap: [AppComponent]
})
export class AppModule { }
