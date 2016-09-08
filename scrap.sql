/*
Navicat MySQL Data Transfer

Source Server         : local-root
Source Server Version : 50525
Source Host           : localhost:3306
Source Database       : scrap

Target Server Type    : MYSQL
Target Server Version : 50525
File Encoding         : 65001

Date: 2016-09-08 13:39:58
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hotel
-- ----------------------------
DROP TABLE IF EXISTS `hotel`;
CREATE TABLE `hotel` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL,
  `star` varchar(80) NOT NULL,
  `city` varchar(60) NOT NULL,
  `district` varchar(60) NOT NULL,
  `address` varchar(60) NOT NULL,
  `phone` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hotel_ctrip
-- ----------------------------
DROP TABLE IF EXISTS `hotel_ctrip`;
CREATE TABLE `hotel_ctrip` (
  `id` int(11) NOT NULL COMMENT '酒店编号',
  `name` varchar(80) NOT NULL COMMENT '酒店名',
  `lat` varchar(20) NOT NULL COMMENT '维度',
  `lon` varchar(20) NOT NULL COMMENT '经度',
  `url` varchar(128) NOT NULL COMMENT '详情链接',
  `img` varchar(128) DEFAULT NULL COMMENT '图片地址',
  `address` varchar(128) NOT NULL COMMENT '酒店地址',
  `score` varchar(10) NOT NULL COMMENT '评分',
  `dpscore` varchar(10) NOT NULL COMMENT '推荐百分比',
  `dpcount` varchar(10) NOT NULL COMMENT '点评人数',
  `short_name` varchar(80) DEFAULT NULL COMMENT '简称',
  `star` varchar(80) NOT NULL COMMENT '星级',
  `star_desc` varchar(80) NOT NULL COMMENT '星级描述',
  `is_single_rec` varchar(10) DEFAULT NULL,
  `city` varchar(60) DEFAULT NULL COMMENT '城市',
  `district` varchar(60) DEFAULT NULL COMMENT '地区',
  `phone` varchar(60) DEFAULT NULL COMMENT '酒店电话',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hotel_elong
-- ----------------------------
DROP TABLE IF EXISTS `hotel_elong`;
CREATE TABLE `hotel_elong` (
  `id` varchar(11) NOT NULL COMMENT '酒店编号',
  `name` varchar(80) DEFAULT NULL COMMENT '酒店名',
  `title` varchar(256) DEFAULT NULL COMMENT '标题',
  `phone` varchar(60) DEFAULT NULL COMMENT '电话',
  `city` varchar(20) DEFAULT NULL COMMENT '城市',
  `city_pinyin` varchar(20) DEFAULT NULL COMMENT '城市拼音',
  `district` varchar(20) DEFAULT NULL COMMENT '区县',
  `address` varchar(128) DEFAULT NULL COMMENT '地址',
  `star` varchar(20) DEFAULT NULL COMMENT '星级',
  `description` varchar(2048) DEFAULT NULL COMMENT '描述',
  `create_time` datetime DEFAULT NULL,
  `rooms` int(11) DEFAULT '0' COMMENT '房间数量',
  `pics` int(11) DEFAULT '0' COMMENT '图片数量',
  `try_times` int(11) DEFAULT '0' COMMENT '重试次数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hotel_elong_pics
-- ----------------------------
DROP TABLE IF EXISTS `hotel_elong_pics`;
CREATE TABLE `hotel_elong_pics` (
  `hotel_id` varchar(11) NOT NULL COMMENT '酒店编号',
  `src` varchar(100) NOT NULL COMMENT '图片链接',
  `orders` int(11) NOT NULL COMMENT '序号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lianjia_zufang_room
-- ----------------------------
DROP TABLE IF EXISTS `lianjia_zufang_room`;
CREATE TABLE `lianjia_zufang_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `room_small_href` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `room_detail_url` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `room_detail_title` varchar(256) DEFAULT NULL COMMENT '详情页面的标题名称',
  `col_where` varchar(256) DEFAULT NULL COMMENT '位置',
  `zone` varchar(10) DEFAULT NULL COMMENT '室厅',
  `meters` varchar(10) DEFAULT NULL COMMENT '平米',
  `price` varchar(10) DEFAULT NULL COMMENT '价格(元/月)',
  `col_look` varchar(10) DEFAULT NULL COMMENT '几人看过房',
  `tags` varchar(256) DEFAULT NULL COMMENT '标签',
  `room_detail_sub_title` varchar(256) DEFAULT NULL COMMENT '副标题名称',
  `price_tag` varchar(256) DEFAULT NULL COMMENT '价格标签',
  `zf_room` varchar(256) DEFAULT NULL COMMENT '租房信息',
  `base_content` varchar(256) DEFAULT NULL COMMENT '基本属性',
  `feature_tag` varchar(256) DEFAULT NULL COMMENT '房源特色标签',
  `feature_content` varchar(512) DEFAULT NULL COMMENT '房源特色内容',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1338 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lianjia_zufang_room_img
-- ----------------------------
DROP TABLE IF EXISTS `lianjia_zufang_room_img`;
CREATE TABLE `lianjia_zufang_room_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `img_src` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `img_desc` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11596 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for proxy_ip
-- ----------------------------
DROP TABLE IF EXISTS `proxy_ip`;
CREATE TABLE `proxy_ip` (
  `ip` varchar(50) NOT NULL COMMENT 'IP',
  `port` varchar(10) NOT NULL COMMENT 'PORT',
  `city` varchar(50) DEFAULT NULL COMMENT '归属城市',
  `protocl` varchar(10) DEFAULT NULL COMMENT '协议HTTP/HTTPS',
  `speed` decimal(10,3) DEFAULT NULL COMMENT '速度',
  `resp` decimal(10,3) DEFAULT NULL COMMENT '连接速度',
  `durance` decimal(10,2) DEFAULT NULL COMMENT '生存时间',
  `get_time` datetime DEFAULT NULL COMMENT '探测时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`ip`,`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for room_elong
-- ----------------------------
DROP TABLE IF EXISTS `room_elong`;
CREATE TABLE `room_elong` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '房型编号',
  `hotel_id` varchar(11) NOT NULL COMMENT '酒店编号',
  `name` varchar(30) NOT NULL COMMENT '房型名称',
  `size` varchar(20) DEFAULT NULL COMMENT '面积',
  `bed` varchar(20) DEFAULT NULL COMMENT '床型',
  `price` int(11) DEFAULT NULL COMMENT '价格',
  `pic` varchar(100) DEFAULT NULL COMMENT '房型图片',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pk_room_elong` (`hotel_id`,`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=88148 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for room_elong_price
-- ----------------------------
DROP TABLE IF EXISTS `room_elong_price`;
CREATE TABLE `room_elong_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `room_id` int(11) NOT NULL COMMENT '房型编号',
  `hotel_id` varchar(11) NOT NULL COMMENT '酒店编号',
  `name` varchar(30) NOT NULL COMMENT '房型名称',
  `price` int(11) NOT NULL COMMENT '价格',
  `price_day` date NOT NULL COMMENT '价格日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pk_room_elong_price` (`room_id`,`price_day`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7538 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiaozhu_zufang_room
-- ----------------------------
DROP TABLE IF EXISTS `xiaozhu_zufang_room`;
CREATE TABLE `xiaozhu_zufang_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `detail_title` varchar(256) DEFAULT NULL COMMENT '详情页面的标题名称',
  `detail_url` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `detail_img_href` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `coordinate_x` varchar(10) DEFAULT NULL COMMENT '维度',
  `coordinate_y` varchar(10) DEFAULT NULL COMMENT '经度',
  `price` varchar(10) DEFAULT NULL COMMENT '价格(元/每晚)',
  `em_comment` varchar(256) DEFAULT NULL COMMENT '点评条数',
  `em_address` varchar(256) DEFAULT NULL COMMENT '出租地址',
  `right_num` varchar(256) DEFAULT NULL COMMENT '评分',
  `rental_type` varchar(256) DEFAULT NULL COMMENT '出租类型',
  `capacity` varchar(256) DEFAULT NULL COMMENT '宜住人数',
  `bed_num` varchar(256) DEFAULT NULL COMMENT '床数',
  `room_meters` varchar(256) DEFAULT NULL COMMENT '面积',
  `room_huxing` varchar(256) DEFAULT NULL COMMENT '户型',
  `bed_size_str` varchar(256) DEFAULT NULL COMMENT '床描述',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1504 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiaozhu_zufang_room_attr
-- ----------------------------
DROP TABLE IF EXISTS `xiaozhu_zufang_room_attr`;
CREATE TABLE `xiaozhu_zufang_room_attr` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `attr_type` varchar(256) DEFAULT NULL COMMENT '属性类型',
  `attr_content` varchar(2048) DEFAULT NULL COMMENT '属性内容描述',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7787 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiaozhu_zufang_room_img
-- ----------------------------
DROP TABLE IF EXISTS `xiaozhu_zufang_room_img`;
CREATE TABLE `xiaozhu_zufang_room_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `small_img_src` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `big_img_src` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `img_desc` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33256 DEFAULT CHARSET=utf8;
