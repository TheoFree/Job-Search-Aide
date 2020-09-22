import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { ArticlesService } from 'src/app/services/articles.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ActivatedRoute } from '@angular/router'
@Component({
  selector: 'app-article-display',
  templateUrl: './article-display.component.html',
  styleUrls: ['./article-display.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class ArticleDisplayComponent implements OnInit {
  category = '';
  genre = '';
  constructor(private AS: ArticlesService, private MS: NgbModal, private AR: ActivatedRoute) {

  }

  articles = [];
  pg = 0;
  orderDesc = true;
  orderIndicator = "Newest"
  totalArticleCount = 0;
  queryTerms = "";
  searchFlag = false;
  getArticles = (pg: number) => {
    // console.log("calledGet");
    const ord = this.orderDesc ? 'DESC' : 'ASC';
    this.searchFlag = false;
    this.AS.getArticles(this.genre, pg, ord).subscribe(res => {
      // console.log(res)
      this.articles = res.articles;
      this.totalArticleCount = res.count;

    })
    return this.articles;
  }
  searchSubmit = (pg: number) => {
    const ord = this.orderDesc ? 'DESC' : 'ASC';
    this.searchFlag = true;
    this.AS.searchArticles(this.genre, this.queryTerms, pg, ord).subscribe(res => {
      this.articles = res.articles;
      this.totalArticleCount = res.count;
    })
    return this.articles
  }
  articlesDateReverse = (): any[] => {
    this.orderDesc = !this.orderDesc;
    this.orderIndicator = this.orderDesc ? "Newest" : "Oldest"
    this.searchFlag ? this.searchSubmit(0) : this.getArticles(0);
    this.pg = 0;
    return this.articles
  }
  articlesPageNext = (): any[] => this.pg > (this.totalArticleCount - 20)? this.articles : this.searchFlag ? this.searchSubmit(this.pg += 20) : this.getArticles(this.pg += 20);
  articlesPagePrev = (): any[] => this.pg < 20 ? this.articles : this.searchFlag ? this.searchSubmit(this.pg -= 20) : this.getArticles(this.pg -= 20);
  articleClick = (content) => this.MS.open(content, { ariaLabelledBy: 'article-description', size: 'lg' });
  ngOnInit(): void {
    this.AR.params.subscribe(params => {
      this.AS.setCategoryANDGenre([params.category, params.genre]);
      this.category = params.category;
      this.genre = params.genre;
      this.getArticles(0);
    })

  }

}
