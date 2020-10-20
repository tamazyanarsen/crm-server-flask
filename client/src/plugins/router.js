import App from "@/App";
import VueRouter from 'vue-router';
import Test from "@/components/Test";

const routes = [
    { path: '/', component: App },
    { path: '/test', component: Test }
]

export default new VueRouter({
    routes // сокращённая запись для `routes: routes`
})
