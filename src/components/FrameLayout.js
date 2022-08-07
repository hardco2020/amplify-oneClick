import React, { useEffect, useState }  from 'react';
import { connect } from 'react-redux' 
import { AppLayout, Header, Box, TopNavigation, SideNavigation, BreadcrumbGroup} from '@amzn/awsui-components-react/polaris';
import {withTranslation} from 'react-i18next'
import { breadcrumbItems } from '../utils/breadcrumbItems';
import { navigationItems } from '../utils/navigationItems';
import { useHistory } from 'react-router-dom';

const mapStateToProps = state => {
  return { session: state.session }
}

const MapDispatchTpProps = (dispatch) => {
    return {
        changeLang: (key)=>dispatch({type: 'change_language',data: key})
    }
  }


const FrameLayout = ({t, changeLang, breadcrumb, component}) => {
    const history = useHistory();
    const [activeHref, setActiveHref] = useState('/')
    const _header_side = {
        href: "/",
        text: t("Out of Box AI Demo")
    }

    useEffect(() => {
      console.log(history);
      setActiveHref(history.location.pathname);
    }, [])
    
    const navigation =  
        <SideNavigation 
            activeHref={activeHref}
            header={_header_side} 
            items={navigationItems(t)} 
        />
    const breadcrumbGroup = <BreadcrumbGroup items={breadcrumbItems(t,breadcrumb)} />
    return(
        <>
        <div className="test" style={{position:"sticky", zIndex:"999"}} >
        <TopNavigation
        cla
      identity={{
        href: "#",
        title: "ISV MLOPS",
        // logo: {
        //   src:
        //     "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iNDNweCIgaGVpZ2h0PSIzMXB4IiB2aWV3Qm94PSIwIDAgNDMgMzEiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgIDxnIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxyZWN0IGZpbGw9IiMyMzJmM2UiIHN0cm9rZT0iI2Q1ZGJkYiIgeD0iMC41IiB5PSIwLjUiIHdpZHRoPSI0MiIgaGVpZ2h0PSIzMCIgcng9IjIiPjwvcmVjdD4KICAgICAgICA8dGV4dCBmb250LWZhbWlseT0iQW1hem9uRW1iZXItUmVndWxhciwgQW1hem9uIEVtYmVyIiBmb250LXNpemU9IjEyIiBmaWxsPSIjRkZGRkZGIj4KICAgICAgICAgICAgPHRzcGFuIHg9IjkiIHk9IjE5Ij5Mb2dvPC90c3Bhbj4KICAgICAgICA8L3RleHQ+CiAgICA8L2c+Cjwvc3ZnPgo=",
        //   alt: "Service"
        // }
      }}
      utilities={[
        {
          type: "button",
          text: "Panorama",
          href: "https://aws.amazon.com/panorama/",
          external: true,
          externalIconAriaLabel: " (opens in a new tab)"
        },
        {
          type: "menu-dropdown",
          iconName: "settings",
          ariaLabel: "Settings",
          onItemClick:  (e)=>changeLang(e.detail.id),
          items: [
            {
              
              id: "zh",
              text: "簡體中文"
            },
            {
              id: "en",
              text: "English"
            },
            {
                id: "zh_tw",
                text: "繁體中文"
              }
          ]
        }
      ]}
      i18nStrings={{
        searchIconAriaLabel: "Search",
        searchDismissIconAriaLabel: "Close search",
        overflowMenuTriggerText: "More",
        overflowMenuTitleText: "All",
        overflowMenuBackIconAriaLabel: "Back",
        overflowMenuDismissIconAriaLabel: "Close menu"
      }}
    />
        </div>
      <AppLayout
        headerSelector=".test"
        navigation={navigation}
        breadcrumbs={breadcrumbGroup}
        content={component}
      >
      </AppLayout>
      </>
    )
}


// class  FrameLayout extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//     }
//   }
//   componentDidMount(){
//   }
  

//   componentWillUnmount(){

//   }
  
//   render(){
//     const {
//         props: {t,breadcrumb,url1,url2}
//     } = this;

//     const _header_side = {
//         href: "/",
//         text: t("Out of Box AI Demo")
//     }



//     const navigation =  
//         <SideNavigation 
//             activeHref={`/${breadcrumb}`}
//             header={_header_side} 
//             items={navigationItems(t)} 
//             // onFollow={ event => {
//             //     if (!event.detail.external) {
//             //     //   setActiveHref(event.detail.href);
//             //     }
//             // }}
//         />
//     const breadcrumbGroup = <BreadcrumbGroup items={breadcrumbItems(t,breadcrumb,url1,url2)} />

//     const mainContent = this.props.component
//     return(
//         <>
//         <div className="test" style={{position:"sticky", zIndex:"999"}} >
//         <TopNavigation
//         cla
//       identity={{
//         href: "#",
//         title: "ISV MLOPS",
//         // logo: {
//         //   src:
//         //     "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iNDNweCIgaGVpZ2h0PSIzMXB4IiB2aWV3Qm94PSIwIDAgNDMgMzEiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgIDxnIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxyZWN0IGZpbGw9IiMyMzJmM2UiIHN0cm9rZT0iI2Q1ZGJkYiIgeD0iMC41IiB5PSIwLjUiIHdpZHRoPSI0MiIgaGVpZ2h0PSIzMCIgcng9IjIiPjwvcmVjdD4KICAgICAgICA8dGV4dCBmb250LWZhbWlseT0iQW1hem9uRW1iZXItUmVndWxhciwgQW1hem9uIEVtYmVyIiBmb250LXNpemU9IjEyIiBmaWxsPSIjRkZGRkZGIj4KICAgICAgICAgICAgPHRzcGFuIHg9IjkiIHk9IjE5Ij5Mb2dvPC90c3Bhbj4KICAgICAgICA8L3RleHQ+CiAgICA8L2c+Cjwvc3ZnPgo=",
//         //   alt: "Service"
//         // }
//       }}
//       utilities={[
//         {
//           type: "button",
//           text: "Panorama",
//           href: "https://aws.amazon.com/panorama/",
//           external: true,
//           externalIconAriaLabel: " (opens in a new tab)"
//         },
//         // {
//         //   type: "button",
//         //   iconName: "notification",
//         //   title: "Notifications",
//         //   ariaLabel: "Notifications (unread)",
//         //   badge: true,
//         //   disableUtilityCollapse: false
//         // },
//         {
//           type: "menu-dropdown",
//           iconName: "settings",
//           ariaLabel: "Settings",
//           onItemClick:  (e)=>this.props.changeLang(e.detail.id),
//           items: [
//             {
              
//               id: "zh",
//               text: "簡體中文"
//             },
//             {
//               id: "en",
//               text: "English"
//             },
//             {
//                 id: "zh_tw",
//                 text: "繁體中文"
//               }
//           ]
//         }
//       ]}
//       i18nStrings={{
//         searchIconAriaLabel: "Search",
//         searchDismissIconAriaLabel: "Close search",
//         overflowMenuTriggerText: "More",
//         overflowMenuTitleText: "All",
//         overflowMenuBackIconAriaLabel: "Back",
//         overflowMenuDismissIconAriaLabel: "Close menu"
//       }}
//     />
//         </div>
//       <AppLayout
//         headerSelector=".test"
//         navigation={navigation}
//         breadcrumbs={breadcrumbGroup}
//         content={mainContent}
//       >
//       </AppLayout>
//       </>
//     )
//   }
// }

export default connect(mapStateToProps,MapDispatchTpProps)(withTranslation()(FrameLayout));


