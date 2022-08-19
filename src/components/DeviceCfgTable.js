/* eslint-disable no-alert */
/* eslint-disable react/no-multi-comp */

import { API } from 'aws-amplify';
import Table from 'aws-northstar/components/Table';
import StatusIndicator from 'aws-northstar/components/StatusIndicator';
import Button from 'aws-northstar/components/Button';
import Inline from 'aws-northstar/layouts/Inline';


import React from 'react';
import { connect } from 'react-redux'
import { withTranslation } from 'react-i18next'

const mapStateToProps = state => {
  return { session: state.session }
}

const MapDispatchTpProps = (dispatch) => {
  return {
    changeLang: (key) => dispatch({ type: 'change_language', data: key })
  }
}

const columnDefinitions = [
  {
    'id': 'DeviceId',
    width: 300,
    Header: 'UUID',
    accessor: 'DeviceId'
  },
  {
    'id': 'Name',
    width: 400,
    Header: 'Name',
    accessor: 'Name'
  },
  {
    //'AWAITING_PROVISIONING'|'PENDING'|'SUCCEEDED'|'FAILED'|'ERROR'|'DELETING'
    'id': 'ProvisioningStatus',
    width: 200,
    Header: 'UUID',
    accessor: 'ProvisioningStatus',
    Cell: ({ row }) => {
      if (row && row.original) {
        const status = row.original.ProvisioningStatus;
        switch (status) {
          case 'SUCCEEDED':
            return <StatusIndicator statusType='positive'>{status}</StatusIndicator>;
          case 'AWAITING_PROVISIONING':
            return <StatusIndicator statusType='info'>{status}</StatusIndicator>;
          case 'PENDING':
            return <StatusIndicator statusType='info'>{status}</StatusIndicator>;
          case 'DELETING':
            return <StatusIndicator statusType='warning'>{status}</StatusIndicator>;
          case 'FAILED':
            return <StatusIndicator statusType='negative'>{status}</StatusIndicator>;
          case 'ERROR':
            return <StatusIndicator statusType='negative'>{status}</StatusIndicator>;
          default:
            return <StatusIndicator statusType='info'>{status}</StatusIndicator>;
        }
      }
      return null;
    }

  },
  {
    'id': 'CreatedTime',
    width: 300,
    Header: 'UUID',
    accessor: 'CreatedTime'
  },
  // {
  //     'id': 'core_arn',
  //     width: 200,
  //     Header: 'arn',
  //     accessor: 'core_arn'
  // },
  // {
  //     'id': 'type',
  //     width: 200,
  //     Header: 'type',
  //     accessor: 'type'
  // },
  // {
  //     'id': 'use_gpu',
  //     width: 200,
  //     Header: 'use_gpu',
  //     accessor: 'use_gpu'
  // },
  // {
  //     'id': 'storage',
  //     width: 200,
  //     Header: 'storage',
  //     accessor: 'storage'
  // }
]


class DeviceCfgTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      job_list: [],
      curent: {}
    }
  }

  componentDidMount() {
    // console.log(this.model_list)
    this.setState({ loading: true }, () => {
      this.load_data()
    })
  }


  async load_data() {
    await API.get('backend', '/device').then(res => {
      // await axios.get('/test_cors', {dataType: 'json'}).then(res => {
      console.log('data', res)
      if (res) {
        console.log(res.data)
        var _tmp_data = []
        res.forEach((item) => {
          var _tmp = {}
          _tmp['DeviceId'] = item['DeviceId']
          _tmp['Name'] = item['Name']
          _tmp['ProvisioningStatus'] = item['ProvisioningStatus']
          _tmp['CreatedTime'] = item['CreatedTime']
          _tmp_data.push(_tmp)
        });
        this.setState({ job_list: _tmp_data }, () => {
        })
      }
      this.setState({ loading: false })
      // console.log(this.state.model_list)
      return res
    })
  }



  jump_to_newCfg() {
    this.props.history.push("/NewDeviceConfig")
  }



  render() {
    const {
      props: { t }
    } = this;

    const tableActions = (
      <Inline>
        <Button variant="primary" onClick={() => this.jump_to_newCfg()} disabled={this.state.current.length === 0 ? true : false}>
          {t('Delete Device')}
        </Button>
      </Inline>
    );

    return (

      <Table
        id="DeviceCfgTable"
        actionGroup={tableActions}
        tableTitle={t('Device Config')}
        multiSelect={false}
        columnDefinitions={columnDefinitions}
        items={this.state.job_list}
        onSelectionChange={(item) => { this.setState({ curent: item }) }}
        // getRowId={this.getRowId}
        loading={this.state.loading}
        disableSettings={false}
      // onFetchData={this.handleFetchData}
      />
    )
  }
}


export default connect(mapStateToProps, MapDispatchTpProps)(withTranslation()(DeviceCfgTable));


