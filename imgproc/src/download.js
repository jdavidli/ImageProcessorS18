import React from 'react'
import Button from 'material-ui/Button'

class Download extends React.Component {
  constructor (props) {
    super()
    this.props = props
  }

  handleClick = () => {
    var cleanedPImg = ''
    cleanedPImg = this.props.iDownload[0][0]
    // removes b' from beginning and ' from end
    cleanedPImg = cleanedPImg.slice(2, -1)
    cleanedPImg = 'data:image/jpg;base64,' + cleanedPImg
    console.log(cleanedPImg)
    window.open(cleanedPImg)
  }

  render () {
    return (
      <div>
        <Button onClick={this.handleClick} variant='raised' color='primary'>
          Download
        </Button>
      </div>
    )
  }
}

export default Download
