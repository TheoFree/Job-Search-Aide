import { Component, OnInit } from '@angular/core';
import { ArticlesService } from 'src/app/services/articles.service';

@Component({
  selector: 'app-source-mngr',
  templateUrl: './source-mngr.component.html',
  styleUrls: ['./source-mngr.component.scss']
})
export class SourceMngrComponent implements OnInit {

  constructor(private AS: ArticlesService) { }
  sources = [];
  url = '';
  params = '';
  date = '';
  category = '';
  genre = '';
  getSources=()=>this.AS.getSources().subscribe(res=>{
    this.sources = res[0];
    this.AS.sourcesChanged.emit();
  })
  addSource = ()=>{
    this.AS.addSource(
      this.url,this.params,this.date,this.category,this.genre).subscribe(()=>{
        this.url=this.params=this.date=this.category=this.genre = '';
        this.getSources();
        
      });
      
  }
  removeSource=(id)=>{
    console.log("Component-Remove Call!")
    this.AS.removeSource(id).subscribe(()=>
    // console.log("Component-Remove Finished! Call getSources!")
    this.getSources()
    );
  }
  ngOnInit(): void {
    this.getSources();
  }

}
