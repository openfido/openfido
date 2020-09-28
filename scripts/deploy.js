var path = require('path')
var fs = require('fs')
var mime = require('mime')

let CloudFrontDistributionID
let DeployBucket
let Region

if (process.env.NODE_ENV === 'production') {
    CloudFrontDistributionID = 'E1QGWGOP1SBXD1'
    DeployBucket = 'www.loadinsight.org'
    Region = 'us-east-2'
} else if (process.env.NODE_ENV === 'staging') {
    CloudFrontDistributionID = 'E2JL1I76TWQRZL'
    DeployBucket = 'staging.loadinsight.org'
    Region = 'us-west-1'
} else {
    throw new Error('NODE_ENV not specified')
}

//const InvalidationPaths = ['/index.html', '/favicon.ico', '/service_worker.js', '/static/js/*', '/static/css/*', '/static/media/*', '/assets/*']

const InvalidationPaths = ['/*']
const DeployDir = './build'
const IgnoreFiles = ['.DS_Store']

var AWS = require('aws-sdk')
AWS.config.region = Region

var buildTree = function(dir) {
    const name = dir.replace(DeployDir, '')
    var result = {
        name,
        path: dir,
        files: [],
        dirs: [],
    }

    var list = fs.readdirSync(dir)
    list.forEach(function(file) {
        fullName = dir + '/' + file
        var stat = fs.statSync(fullName)
        if (stat && stat.isDirectory()) {
            const tree = buildTree(fullName)
            result.dirs.push(tree)
        } else {
            if (!IgnoreFiles.includes(file)) result.files.push(file)
        }
    })

    return result
}

var deleteDeployment = function(Bucket, callback) {
    var s3 = new AWS.S3()

    s3.listObjects({ Bucket }, function(err, data) {
        if (err) callback(err)
        else {
            if (data.Contents.length > 0) {
                const Objects = data.Contents.map(i => ({ Key: i.Key }))
                const deleteParams = {
                    Bucket,
                    Delete: {
                        Objects,
                        Quiet: true,
                    },
                }

                s3.deleteObjects(deleteParams, function(err, data) {
                    if (err) callback(err)
                    else callback()
                })
            } else {
                callback()
            }
        }
    })
}

var uploadFiles = function(path, files, Bucket, callback) {
    if (files.length > 0) {
        var file = files[0]
        var filePath = path + '/' + file
        var mimeType = mime.getType(filePath)
        console.log(filePath)
        console.log(mimeType)
        var data = fs.readFileSync(filePath)

        var s3 = new AWS.S3()
        s3.putObject(
            {
                Bucket: Bucket,
                Key: file,
                ContentType: mimeType,
                ACL: 'public-read',
                Body: data,
            },
            function(err, res) {
                if (err) callback(err)
                else {
                    console.log(`Uploaded: ${file}`)
                    files = files.splice(1)
                    uploadFiles(path, files, Bucket, callback)
                }
            }
        )
    } else {
        callback()
    }
}

var uploadDirs = function(dirs, RootBucket, callback) {
    if (dirs.length > 0) {
        var dir = dirs[0]
        var Bucket = RootBucket + dir.name

        var s3 = new AWS.S3()
        console.log(Bucket)

        uploadFiles(dir.path, dir.files, Bucket, function(err) {
            if (err) callback(err)
            else {
                uploadDirs(dir.dirs, RootBucket, function(err) {
                    if (err) callback(err)
                    else {
                        dirs = dirs.splice(1)
                        uploadDirs(dirs, RootBucket, callback)
                    }
                })
            }
        })
    } else {
        callback()
    }
}

var deployDirectory = function(dirTree, RootBucket, callback) {
    uploadFiles(dirTree.path, dirTree.files, RootBucket, function(err) {
        if (err) callback(err)
        else {
            uploadDirs(dirTree.dirs, RootBucket, callback)
        }
    })
}

var randomString = function(length) {
    var text = ''
    var possible =
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for (var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length))
    }
    return text
}

var invalidateDistribution = function(
    distributionId,
    invalidationPaths,
    callback
) {
    var cloudfront = new AWS.CloudFront()
    var callerReference = randomString(10)
    console.log(`Invalidate Reference: ${callerReference}`)
    console.log(invalidationPaths)
    var params = {
        DistributionId: distributionId,
        InvalidationBatch: {
            CallerReference: callerReference,
            Paths: {
                Quantity: invalidationPaths.length,
                Items: invalidationPaths,
            },
        },
    }
    cloudfront.createInvalidation(params, function(err, data) {
        if (err) callback(err)
        else callback()
    })
}

const deployTree = buildTree(DeployDir)
deleteDeployment(DeployBucket, function(err) {
    if (err) error(err)
    else {
        console.log('Deployment deleted')
        console.log('Starting deploy...')
        deployDirectory(deployTree, DeployBucket, function(err) {
            if (err) error(err)
            else {
                console.log('Files Deployed')
                console.log('Invalidating Distribution...')
                invalidateDistribution(
                    CloudFrontDistributionID,
                    InvalidationPaths,
                    function(err) {
                        if (err) {
                            error(err)
                        } else {
                            console.log('Deployment invalidated')
                        }
                    }
                )
            }
        })
    }
})

const error = function(err) {
    console.error('ERROR: ', err.message)
    process.exit(1)
}
