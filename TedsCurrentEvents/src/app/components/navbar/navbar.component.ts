import { Component, OnInit } from '@angular/core';
import { ArticlesService } from 'src/app/services/articles.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  constructor(private AS:ArticlesService) { }
  public categories_genres = [];
  buildNavbar=()=>{
    this.AS.getCategoriesANDGenres().subscribe(res=>this.categories_genres = res)
  }
  ngOnInit(): void {
    this.buildNavbar();
  }

}
