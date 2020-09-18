import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { ArticleDisplayComponent } from './components/article-display/article-display.component';
import { SourceMngrComponent } from './components/source-mngr/source-mngr.component';

const routes: Routes = [
  {
    path:"home",
    component:HomeComponent
  },
  {
    path:":category/:genre",
    component:ArticleDisplayComponent
  },
  {
    path:"source-manager",
    component:SourceMngrComponent
  },
  {
    path:"**",
    pathMatch:"full",
    redirectTo:"home"
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
