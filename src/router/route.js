import Home from "@/pages/home";
import AuthenticationLogin from "@/pages/authentication";
import DeviceDetectionPage from "@/pages/deviceDetectionDetail";
import WarningDetail from "@/pages/warningDetail";
import MessageCenter from "@/pages/messageCenter";
import User from "@/pages/user";

const routeList = [
  {
    path: "/login",
    component: AuthenticationLogin,
    title: "登录页",
    name: "login",
  },
  {
    path: "/",
    component: Home,
    title: "首页",
    name: "home",
  },
  {
    path: "/deviceDetectionPage",
    component: DeviceDetectionPage,
    title: "设备监测",
    name: "deviceDetectionPage",
  },

  {
    path: "/warningDetail",
    component: WarningDetail,
    title: "报警详情",
    name: "warningDetail",
  },
  {
    path: "/messageCenter",
    component: MessageCenter,
    title: "消息中心",
    name: "messageCenter",
  },
  {
    path: "/user",
    component: User,
    title: "我的",
    name: "user",
  },
];

export default routeList;
