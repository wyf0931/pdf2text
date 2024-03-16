import {
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements,
  Route,
  Navigate,
} from 'react-router-dom'
import Home from '../page/home'
import PdfToText from '../page/pdf-to-text'

// import MessageCenter from '@/pages/messageCenter'
// import User from '@/pages/user'

// import AuthenticationLogin from '@/pages/authentication'
// import DeviceDetectionPage from '@/pages/deviceDetectionDetail'
// import WarningDetail from '@/pages/warningDetail'
// import Layout from '@/pages/layout'
// import ProjectDailyDetails from '@/pages/projectDailyDetails'
// import WarningList from '@/pages/projectDailyDetails/components/warningList'
// import EmergencyCommandRecord from '@/pages/emergencyCommandRecord'

const BrowserRouter = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
      <Route path="/pdfToText" element={<PdfToText />} />
      {/* <Route index element={<Navigate to="/home" />} /> */}
      {/* <Route path="/home" element={<Home />} /> */}
      {/* <Route path="/login" element={<AuthenticationLogin />} /> */}
      {/* <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/home" />} />
        <Route path="/home" element={<Home />} />
        <Route path="/messageCenter" element={<MessageCenter />} />
        <Route path="/user" element={<User />} />
        <Route path="/deviceDetectionPage" element={<DeviceDetectionPage />} />
        <Route path="/warningDetail/:id" element={<WarningDetail />} />
        <Route
          path="/projectDailyDetails/:id"
          element={<ProjectDailyDetails />}
        />
        <Route path="/warningList/:id" element={<WarningList />} />
        <Route
          path="/emergencyCommandRecord"
          element={<EmergencyCommandRecord />}
        />
      </Route> */}
    </>,
  ),
)

const GlobalRouter = () => {
  return <RouterProvider router={BrowserRouter}></RouterProvider>
}

export default GlobalRouter
// {routeList.map((item) => {
//   return (
//     <Route
//       key={item.name}
//       path={item.path}
//       element={<item.component />}
//     ></Route>
//   );
// })}
