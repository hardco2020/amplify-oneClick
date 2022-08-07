import Table from 'aws-northstar/components/Table';
// import StatusIndicator from 'aws-northstar/components/StatusIndicator';
import Button from 'aws-northstar/components/Button';
import Inline from 'aws-northstar/layouts/Inline';

import { useHistory } from 'react-router-dom';
import React,{useEffect,useState}  from 'react';
import { connect } from 'react-redux' 

import axios from 'axios'
import { API } from 'aws-amplify'; 

import {withTranslation} from 'react-i18next'
const mapStateToProps = state => {
    return { session: state.session }
  }
  const MapDispatchTpProps = (dispatch) => {
    return {
        changeLang: (key)=>dispatch({type: 'change_language',data: key})
    }
  }

  const columnDefinitions = [
    {
        'id': 'Deployment_ID',
        width: 200,
        Header: 'ID',
        accessor: 'Deployment_ID'
    },
    {
        'id': 'Device_ID',
        width: 200,
        Header: 'Device ID',
        accessor: 'Device_ID'
    },
    {
        'id': 'Camera_ID',
        width: 200,
        Header: 'Camera ID',
        accessor: 'Camera_ID'
    },
    {
        'id': 'Component_Version_ID',
        width: 300,
        Header: 'UUID',
        accessor: 'Component_Version_ID'
    },
    {
        'id': 'Model_Version_ID',
        width: 300,
        Header: 'Camera Name',
        accessor: 'Model_Version_ID'
    },
    // {
    //     'id': 'targetArn',
    //     width: 300,
    //     Header: 'Arn',
    //     accessor: 'targetArn'
    // },
    {
        'id': 'deploymentName',
        width: 300,
        Header: 'APP Name',
        accessor: 'deploymentName'
    },
    // {
    //     'id': 'components',
    //     width: 600,
    //     Header: 'CFG-Components',
    //     accessor: 'components'
    // },
    // {
    //     'id': 'deploymentPolicies',
    //     width: 600,
    //     Header: 'CFG-Policy',
    //     accessor: 'deploymentPolicies'
    // },
    // {
    //     'id': 'iotJobConfigurations',
    //     width: 600,
    //     Header: 'CFG-IoTJob',
    //     accessor: 'iotJobConfigurations'
    // },
]


const DeploymentCfgTable = ({t, changeLang}) =>{
    let history = useHistory();
    const [loading, setLoading] = useState(true);
    const [joblist, setJoblist] = useState([]);
    // const [current, setCurrent] = useState({});
    // console.log(current);
    useEffect(() => {
        const load_data  = async() =>{
            await API.get('backend','/deployment').then(res => {
                console.log(res)
                if (res){
                    console.log(res)
                    let _tmp_data = []
                    res.forEach((item)=>{
                        let _tmp = {}
                        _tmp['Deployment_ID'] = item['DeploymentID']
                        _tmp['Device_ID'] = item['DeviceID']
                        _tmp['Camera_ID'] = item['CameraID']
                        _tmp['Component_Version_ID'] = item['ComponentVersionID']
                        _tmp['Model_Version_ID'] = item['ModelVersionID']
                        _tmp['targetArn'] = item['targetArn']
                        _tmp['deploymentName'] = item['DeploymentName']
                        _tmp['components'] = item['components']
                        _tmp['deploymentPolicies'] = item['deploymentPolicies']
                        _tmp['iotJobConfigurations'] = item['iotJobConfigurations']
                        
                        _tmp_data.push(_tmp)
                    });
        
                    // const test_data =  {
                    //     'Deployment_ID':'cb831c07-2556-4433-ad60-da0720d78113',
                    //     'Device_ID':'123',
                    //     'Camera_ID':'123',
                    //     'Component_Version_ID':'123',
                    //     'Model_Version_ID':'123',
                    //     'targetArn':'123',
                    //     'deploymentName':'123',
                    //     'components':'123',
                    //     'deploymentPolicies':'123',
                    //     'iotJobConfigurations':'123',
                    // }
                    // const test_data_2 =  {
                    //     'Deployment_ID':'cb831c07-2556-4433-ad60-da0720d7811311',
                    //     'Device_ID':'123333',
                    //     'Camera_ID':'123',
                    //     'Component_Version_ID':'123',
                    //     'Model_Version_ID':'123',
                    //     'targetArn':'123',
                    //     'deploymentName':'123',
                    //     'components':'123',
                    //     'deploymentPolicies':'123',
                    //     'iotJobConfigurations':'123',
                    // }
                    // _tmp_data.push(test_data);
                    // _tmp_data.push(test_data_2);
                    console.log(_tmp_data);
                    setJoblist(_tmp_data);
                    setLoading(false);
                }
                // console.log(this.state.model_list)
                return res.data
            })
        }
        load_data();
    }, [])

    const jump_to_newCfg = () =>{
        history.push("/NewDeployConfig");
    }

    const tableActions = (
                <Inline>
                    <Button variant="primary" onClick={() => jump_to_newCfg()}>
                        {t('New Deployment')}
                    </Button>
                </Inline>
            );
    return(
        <>
        <Button onClick={()=>changeLang('en')}>test</Button>
        <Table
        id = "DepCfgTable"
        actionGroup={tableActions}
        tableTitle={t('Deployment Config')}
        columnDefinitions={columnDefinitions}
        items={joblist}
        disableRowSelect="true"
        disableGroupBy={false}
        defaultGroups={['Deployment_ID']}
        loading={loading}
        />
        </>
    )
}

export default connect(mapStateToProps,MapDispatchTpProps)(withTranslation()(DeploymentCfgTable));


