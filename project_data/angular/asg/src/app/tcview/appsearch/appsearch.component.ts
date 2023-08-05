import { Component, OnInit} from '@angular/core';
import { TcService } from '@app/_services/tc.service';
import {  } from '@angular/core';
import { IApp } from '@app/_interfaces/IApp';

@Component({
  selector: 'app-appsearch',
  templateUrl: './appsearch.component.html',
  styleUrls: ['./appsearch.component.css']
})
export class AppsearchComponent implements OnInit {
  constructor(
    private tcService:TcService
    ) { }
  foundList :any
  query:string;

  ngOnInit(): void {
  
  }
  
  searchQ(query) {
    this.foundList = []
    this.tcService.Search(query).subscribe(
      data => this.foundList = data
    )
  
  }

}


