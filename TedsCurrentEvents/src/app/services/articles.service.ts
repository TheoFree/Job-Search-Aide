import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ArticlesService {

  constructor(private http: HttpClient) { }
  
  sortDate=(articles):any[]=>articles.sort((a,b)=>Date.parse(b[2]) - Date.parse(a[2]));
  sortDateReverse=(articles):any[]=>articles.reverse();
  
  getArticles=(genre,pg=0,ord='DESC'):Observable<any>=>{
    return this.http.get("http://127.0.0.1:5000/articles/"+genre+'/list?pg='+pg.toString()+'&ord='+ord);
  }
  searchArticles=(genre,searchTerm="",pg=0,ord='DESC'):Observable<any>=>this.http.get('http://127.0.0.1:5000/articles/'+genre+'/search',{
    params: new HttpParams()
    .set('q',searchTerm)
    .set('pg', pg.toString())
    .set('ord',ord)})
    // '?q='+searchTerm+'&pg='+pg+'&ord='+ord);

}