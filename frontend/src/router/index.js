import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import LoginView from '@/views/LoginView.vue'
import VotingView from '@/views/VotingView.vue'
import ResultsView from '@/views/ResultsView.vue'
import NotFoundView from '@/views/NotFoundView.vue'

const routes = [
  { path: '/', name: 'login', component: LoginView },
  { path: '/votacion', name: 'votacion', component: VotingView, meta: { requiereVerificacion: true } },
  { path: '/resultados', name: 'resultados', component: ResultsView },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiereVerificacion && !auth.verificado) {
    return { name: 'login' }
  }
})

export default router
