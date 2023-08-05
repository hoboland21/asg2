import { Component, OnInit, OnChanges, SimpleChanges, Input } from '@angular/core';
import { TcService } from '@app/_services/tc.service';

@Component({
  selector: 'app-nrelic',
  templateUrl: './nrelic.component.html',
  styleUrls: ['./nrelic.component.css']
})
export class NrelicComponent implements OnInit, OnChanges {
  @Input() flag:boolean;
  NRList : [];
  constructor(private tcService : TcService) { 
    
  }

  ngOnInit(): void {
    this.tcService.getNRAlerts().subscribe(
      list => this.NRList = list
    )
  }
  ngOnChanges(changes: SimpleChanges) {
    this.NRList = []
    this.tcService.getNRAlerts().subscribe(
     list => this.NRList = list
   )
  }
}
