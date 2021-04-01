 'use strict'

const path = require('path');
const webpack = require('webpack');
const {VueLoaderPlugin} = require('vue-loader')
const {CleanWebpackPlugin} = require('clean-webpack-plugin');

module.exports = {
    externals: {
        vue: 'Vue',
        axios: 'axios',
    },
    context: path.resolve(__dirname, '.'),
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
    },

    plugins: [
        new CleanWebpackPlugin(),
        new webpack.DefinePlugin({
            'process.env.environ': JSON.stringify(process.env.environ)
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        }),
        new VueLoaderPlugin()
    ],

    module: {
        rules: [
            {
                test: /\.vue$/,
                use: 'vue-loader'
            },
            {
                test: /\.(sc|sa|c)ss$/,
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
                    },
                    {
                        loader: "sass-loader" // compiles Sass to CSS
                    }
                ]
            },
            // {
            //     test: /\.scss$/,
            //     use: [
            //         {
            //             loader: "style-loader" // creates style nodes from JS strings
            //         },
            //         {
            //             loader: "css-loader" // translates CSS into CommonJS
            //         },
            //         {
            //             loader: "sass-loader" // compiles Sass to CSS
            //         }
            //     ]
            // },

            {
                test: /\.(wav|mp3|eot|ttf)$/,
                loader: 'file-loader',
            },
            {
                test: /\.(woff2?|eot|ttf|otf|svg)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                }
            },
        ]
    },
};