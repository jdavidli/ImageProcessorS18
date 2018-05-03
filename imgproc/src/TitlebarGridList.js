import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import GridList, { GridListTile, GridListTileBar } from 'material-ui/GridList'
import IconButton from 'material-ui/IconButton'
import InfoIcon from '@material-ui/icons/Info'
import Dialog, { DialogTitle, DialogContent, DialogContentText} from 'material-ui/Dialog'
import {AreaChart, Area, XAxis, YAxis} from 'recharts'

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper
  },
  gridList: {
    width: 500
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)'
  }
})

class TitlebarGridList extends React.Component {
  constructor (props) {
    super()
    this.props = props
    this.state = {
      open: false,
      open2: false
    }
  }

  handleClickOpen = () => {
    this.setState({ open: true })
  };

  handleClose = () => {
    this.setState({ open: false })
  };

  handleClickOpen2 = () => {
    this.setState({ open2: true })
  };

  handleClose2 = () => {
    this.setState({ open2: false })
  };

  render () {
    const { classes } = this.props
    const origTileData = []
    for (var i = 0; i < this.props.oImgParent.length; i++) {
      origTileData.push({img: this.props.oImgParent[i],
      uptime: this.props.uTime, upsize: this.props.uSize[i]})
      console.log(i)
    }

    const procTileData = []
    for (var j = 0; j < this.props.pImgParent.length; j++) {
      var cleanedImg = ''
      cleanedImg = this.props.pImgParent[j][0]
      // removes b' from beginning and ' from end
      cleanedImg = cleanedImg.slice(2, -1)
      cleanedImg = 'data:image/jpg;base64,' + cleanedImg
      procTileData.push({img: cleanedImg,
      proctime: this.props.pTime[j], upsize: this.props.uSize[j]})
      console.log(i)
    }

    const tileData = [
      {
        img: this.props.oImgParent,
        uptime: this.props.uTime,
        upsize: this.props.uSize,
        which: 'orig'
      }
    ]
    const tileData2 = [
      {
        img: this.props.pImgParent,
        proctime: this.props.pTime,
        upsize: this.props.uSize,
        which: 'proc'
      }
    ]

    // graphing
    const preOData = this.props.oHist[0]
    const prePData = this.props.pHist[0]
    // const lgProps = [{ dataKey: 'R', values: preOData}]
    // console.log(lgProps)
    var oData = []
    // var oJSON = {}
    for (var m in preOData) {
      oData.push({'R': preOData[m]})
    }
    var pData = []
    for (var n in prePData) {
      pData.push({'R': prePData[n]})
    }
    // console.log(oData)

    return (
      <div className={classes.root}>
        <GridList cellHeight={200} className={classes.gridList}>
          <GridListTile key='Subheader' cols={1} style={{ height: 'auto' }} />
          {origTileData.map((tile, i) => (
            <GridListTile key={tile.img + i}>
              <img src={tile.img} />
              <GridListTileBar
                actionIcon={
                  <IconButton className={classes.icon} onClick={this.handleClickOpen}>
                    <Dialog
                      open={this.state.open}
                      onClose={this.handleClose}
                      aria-labelledby='alert-dialog-title'
                      aria-describedby='alert-dialog-description'
                    >
                      <DialogTitle id='alert-dialog-title'>{'Original Image Information'}</DialogTitle>
                      <DialogContent>
                        <DialogContentText id='alert-dialog-description'>
                          <AreaChart width={550} height={400} data={oData}
                            margin={{top: 10, right: 10, left: 0, bottom: 0}}>
                            <XAxis ticks={[0, 255]} />
                            <YAxis />
                            <Area type='monotone' dataKey='R' stackId='1' stroke='#8884d8' fill='#8884d8' />
                          </AreaChart>
            Uploaded time: {tile.uptime}
                          <br />
            Image size: {tile.upsize}
                        </DialogContentText>
                      </DialogContent>
                    </Dialog>
                    <InfoIcon />
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>

        <GridList cellHeight={200} className={classes.gridList}>
          <GridListTile key='Subheader2' cols={1} style={{ height: 'auto' }} />
          {procTileData.map((tile, j) => (
            <GridListTile key={tile.img + j}>
              <img src={tile.img} />
              <GridListTileBar
                actionIcon={
                  <IconButton className={classes.icon} onClick={this.handleClickOpen2}>
                    <Dialog
                      open={this.state.open2}
                      onClose={this.handleClose2}
                      aria-labelledby='alert-dialog-title2'
                      aria-describedby='alert-dialog-description2'
                    >
                      <DialogTitle id='alert-dialog-title2'>{'Processed Image Information'}</DialogTitle>
                      <DialogContent>
                        <DialogContentText id='alert-dialog-description2'>
                          <AreaChart width={550} height={400} data={pData}
                            margin={{top: 10, right: 10, left: 0, bottom: 0}}>
                            <XAxis ticks={[0, 255]} />
                            <YAxis />
                            <Area type='monotone' dataKey='R' stackId='1' stroke='#8884d8' fill='#8884d8' />
                          </AreaChart>
            Processing time: {tile.proctime}
                          <br />
            Image size: {tile.upsize}
                        </DialogContentText>
                      </DialogContent>
                    </Dialog>
                    <InfoIcon />
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>
      </div>
    )
  }
}

TitlebarGridList.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(TitlebarGridList)
