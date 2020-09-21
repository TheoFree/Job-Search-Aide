import { EventEmitter, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ArticlesService {

  constructor(private http: HttpClient) { }
  private genre: String = '';
  private category: String = '';
  private genres: [String];
  private categories: [String];
  sortDate = (articles): any[] => articles.sort((a, b) => Date.parse(b[2]) - Date.parse(a[2]));
  sortDateReverse = (articles): any[] => articles.reverse();
  setCategoryANDGenre = (catGen: [any, any]) => [this.category, this.genre] = catGen;
  getCategoriesANDGenres = (): Observable<any> => this.http.get('http://127.0.0.1:5000/sources/genres')
  getGenre = () => [this.category, this.genre];
  getArticles = (genre, pg = 0, ord = 'DESC'): Observable<any> => {
    return this.http.get('http://127.0.0.1:5000/articles/' + this.category + '/' + this.genre + '/list?pg=' + pg.toString() + '&ord=' + ord);
  }
  searchArticles = (genre, searchTerm = "", pg = 0, ord = 'DESC'): Observable<any> => this.http.get('http://127.0.0.1:5000/articles/' + this.category + '/' + this.genre + '/search', {
    params: new HttpParams()
      .set('q', searchTerm)
      .set('pg', pg.toString())
      .set('ord', ord)
  })
  // '?q='+searchTerm+'&pg='+pg+'&ord='+ord);
  getSources = () => this.http.get('http://127.0.0.1:5000/sources/');
  addSource = (url,params,date,category,genre)=> this.http.post('http://127.0.0.1:5000/sources/add/'+url+'&'+params+'&'+date+'&'+category+'&'+genre,{})

  removeSource =(id)=> this.http.delete(`http://127.0.0.1:5000/sources/delete/${id}`)

  sourcesChanged:EventEmitter<any> = new EventEmitter();
}