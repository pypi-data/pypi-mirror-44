<template>
    <div class="tags" v-if="showTags">
        <ul>
            <li class="tags-li" v-for="(item,index) in tagsList" :class="{'active': isActive(item.path)}" :key="index">
                <router-link :to="item.path" class="tags-li-title">
                    {{item.getTitle()}}
                </router-link>
                <span class="tags-li-icon" @click="closeTag(index)"><i class="el-icon-close"></i></span>
            </li>
        </ul>
        <div class="tags-close-box">
            <el-dropdown @command="handleTags">
                <el-button size="mini" type="primary">
                    {{ $t('label.tagOptions') }}<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu size="small" slot="dropdown">
                    <el-dropdown-item command="closeOthers">{{ $t('label.closeOtherTags') }}</el-dropdown-item>
                    <el-dropdown-item command="closeAll">{{ $t('label.closeAllTags') }}</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </div>
</template>

<script>
    import utils from './utils'
    import menu from '../menu'

    const __homePage = "/dashboard"
    const __getDefaultPageFromMenu = function(currentMenu, level=1) {
        if (level <= 0 || level > 3) {
            return __homePage
        }
        currentMenu.forEach((item, i) => {
            if (item.subs) {
                if (level < 3) {
                return __getDefaultPageFromMenu(item.subs, level + 1)
                }
            } else {
                if (item.path && item.component) {
                    if (item.path != '/403' && item.path != '/404' && item.path != '/') {
                        if (item.default) {
                            return item.path
                        }
                    }
                }
            }
        })
        return __homePage
    }
    export default {
        data() {
            return {
                tagsList: [],
            }
        },
        methods: {
            isActive(path) {
                return path.split("?")[0].toLowerCase() === this.$route.fullPath.split("?")[0].toLowerCase();
            },
            // 关闭单个标签
            closeTag(index) {
                if (index == 0 && this.tagsList.length == 1 && this.homePage == this.tagsList[index].path) {
                    // cannot close the only home tab
                    return
                }
                const delItem = this.tagsList.splice(index, 1)[0];
                const item = this.tagsList[index] ? this.tagsList[index] : this.tagsList[index - 1];
                if (item) {
                    this.$router.push(item.path);
                } else {
                    this.$router.push('/');
                }
            },
            // 关闭全部标签
            closeAll() {
                var activeHomeItem = null
                this.tagsList.forEach((item, i) => {
                    if (this.homePage == item.path && this.isActive(item.path) ) {
                        activeHomeItem = item
                        return
                    }
                })
                this.tagsList = activeHomeItem?[activeHomeItem]:[] 
                if (activeHomeItem) {
                    this.$bus.$emit('tags', this.tagsList);
                } else {
                    this.$router.push('/');
                }
            },
            // 关闭其他标签
            closeOthers(){
                const curItem = this.tagsList.filter(item => {
                    return this.isActive(item.path)
                })
                this.tagsList = curItem;
                this.$bus.$emit('tags', this.tagsList);
            },
            // 设置标签
            setTags(route){
                const isExist = this.tagsList.some(item => {
                    return item.path.toLowerCase() === route.fullPath.split("?")[0].toLowerCase();
                })
                if(!isExist){
                    if(this.tagsList.length >= 8){
                        this.tagsList.shift();
                    }
                    this.tagsList.push({
                        getTitle: route.meta.getTitle,
                        path: route.fullPath.split("?")[0],
                        name: route.matched[1].components.default.name,
                    })
                }
                this.$bus.$emit('tags', this.tagsList);
            },
            handleTags(command){
                command === 'closeOthers' ? this.closeOthers() : this.closeAll();
            }
        },
        computed: {
            showTags() {
                return this.tagsList.length > 0;
            },
            homePage() {
                return __getDefaultPageFromMenu(menu, 1)
            },
        },
        watch:{
            $route(newValue, oldValue){
                this.setTags(newValue);
            }
        },
        created(){
            this.setTags(this.$route);
        }
    }

</script>


<style>
    .tags {
        position: relative;
        height: 30px;
        overflow: hidden;
        background: #fff;
        padding-right: 120px;
        box-shadow: 0 5px 10px #ddd;
    }

    .tags ul {
        box-sizing: border-box;
        width: 100%;
        height: 100%;
    }

    .tags-li {
        float: left;
        margin: 3px 5px 2px 3px;
        border-radius: 3px;
        font-size: 12px;
        overflow: hidden;
        cursor: pointer;
        height: 23px;
        line-height: 23px;
        border: 1px solid #e9eaec;
        background: #fff;
        padding: 0 5px 0 12px;
        vertical-align: middle;
        color: #666;
        -webkit-transition: all .3s ease-in;
        -moz-transition: all .3s ease-in;
        transition: all .3s ease-in;
    }

    .tags-li:not(.active):hover {
        background: #f8f8f8;
    }

    .tags-li.active {
        color: #fff;
    }

    .tags-li-title {
        float: left;
        max-width: 80px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        margin-right: 5px;
        color: #666;
    }

    .tags-li.active .tags-li-title {
        color: #fff;
    }

    .tags-close-box {
        position: absolute;
        right: 0;
        top: 0;
        box-sizing: border-box;
        padding-top: 1px;
        text-align: center;
        width: 110px;
        height: 30px;
        background: #fff;
        box-shadow: -3px 0 15px 3px rgba(0, 0, 0, .1);
        z-index: 10;
    }

</style>
