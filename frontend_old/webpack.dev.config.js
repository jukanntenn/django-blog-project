'use strict'

const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require('webpack');
const {VueLoaderPlugin} = require('vue-loader')

module.exports = {
    entry: './src/index.js',
    output: {
        filename: "[name]-[hash].js",
        path: path.resolve(__dirname, 'dist'),
        publicPath: 'http://localhost:8080/'
    },

    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        }),
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
        new VueLoaderPlugin()
    ],

    module: {
        rules: [
            {
                test: /\.css$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'style-loader'
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        }
                    },
                    {
                        loader: 'postcss-loader'
                    }
                ]
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: "style-loader" // creates style nodes from JS strings
                    },
                    {
                        loader: "css-loader" // translates CSS into CommonJS
                    },
                    {
                        loader: "sass-loader" // compiles Sass to CSS
                    }
                ]
            },
            {
                test: /\.vue$/,
                use: 'vue-loader'
            },
            {
                test: /\.(wav|mp3|eot|ttf)$/,
                loader: 'file-loader',
            },
            {
                test: /\.(woff2?|eot|ttf|otf|svg)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    // name: utils.assetsPath('fonts/[name].[hash:7].[ext]')
                }
            },
        ]
    },

    devServer: {
        port: 8081,
        host: '0.0.0.0',
        overlay: {
            errors: true
        },
        hot: true,
        headers: {
            "Access-Control-Allow-Origin": "\*"
        }
    }
};