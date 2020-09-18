import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { HomeComponent } from './components/home/home.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ArticleDisplayComponent } from './components/article-display/article-display.component';
import { FormsModule} from '@angular/forms';
import { NavbarComponent } from './components/navbar/navbar.component';
import { SourceMngrComponent } from './components/source-mngr/source-mngr.component'

@NgModule({
  declarations: [
    AppComponent,
    
    HomeComponent,
    ArticleDisplayComponent,
    NavbarComponent,
    SourceMngrComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
