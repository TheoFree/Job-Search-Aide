import { Component, OnInit } from '@angular/core';
import { Article } from './article.article';
import { ArticlesService } from '../../../services/articles.service'
@Component({
  selector: 'app-tech',
  templateUrl: './tech.component.html',
  styleUrls: ['./tech.component.scss']
})
export class TechComponent implements OnInit {

  constructor(private AS:ArticlesService) { }
  articles = [];
  getArticles=()=>{
    this.AS.getArticles("tech").subscribe(res=>{
      this.articles = res.articles;
     
    })
  }
  ngOnInit(): void {
    this.getArticles();
  }
  

}
