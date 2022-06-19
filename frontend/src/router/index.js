import { createRouter, createWebHistory } from 'vue-router'
import ReadPostView from '../views/ReadPostView.vue'
import Frontpage from '../views/Frontpage.vue'
import BoardView from '../views/BoardView.vue'
import WritePost from '../views/WritePost.vue'
import Home from '../views/Home.vue'

function guardMyroute(to, from, next)
{var isAuthenticated= false;
if(localStorage.getItem('sessionToken')) isAuthenticated = true;
else isAuthenticated= false;
if(isAuthenticated) {next();} 
else {next('/');}
}

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    props: true,
  },
  {
    path: '/frontpage',
    name: 'frontpage',
    beforeEnter : guardMyroute,
    component: Frontpage
  },
  {
    path: '/board/:boardName',
    name: 'board',
    beforeEnter : guardMyroute,
    component: BoardView
  },
  {
    path: '/post/:postId',
    name: 'readPost',
    beforeEnter : guardMyroute,
    component: ReadPostView
  },
  {
    path: '/writepost/:boardName',
    name: 'writePost',
    beforeEnter : guardMyroute,
    component: WritePost
  },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
