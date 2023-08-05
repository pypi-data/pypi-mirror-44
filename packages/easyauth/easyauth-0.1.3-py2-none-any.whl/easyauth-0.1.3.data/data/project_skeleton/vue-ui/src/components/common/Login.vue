<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">{{ $t('page.title') }}</div>
            <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="loginForm.username" :placeholder="$t('placeholder.username')" autocomplete="on">
                        <el-button slot="prepend" icon="el-icon-lx-people" tabindex="-1"></el-button>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" :placeholder="$t('placeholder.password')" autocomplete="off" v-model="loginForm.password" @keyup.enter.native="submitForm('loginForm')">
                        <el-button slot="prepend" icon="el-icon-lx-lock" tabindex="-1"></el-button>
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm('loginForm')">{{ $t('label.loginButton') }}</el-button>
                </div>
                <p class="login-tips"></p>
            </el-form>
        </div>
    </div>
</template>

<script>
    import { Message } from 'element-ui'

    export default {
        data: function(){
            return {
                loginForm: {
                    username: '',
                    password: ''
                },
            }
        },
        computed: {
            rules(){
                let calRules = {
                    username: [
                        { required: true, message: this.$t('message.inputUsername'), trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: this.$t('message.inputPassword'), trigger: 'blur' }
                    ]
                }
                return calRules
            }
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                      this.$easyauth.authentication.login(this.loginForm.username, this.loginForm.password)
                        .then(res => {
                            var redirectUrl = '/'
                            if (this.$route.query && this.$route.query.redirect) {
                                redirectUrl = this.$route.query.redirect
                            }
                            this.$router.push(redirectUrl);
                        })
                        .catch(err => {
                            Message.error({
                                message: [this.$t("message.loginFailed"), ': ', err.data.detail].join("")
                        })
                        })
                    } else {
                        return false;
                    }
                });
            }
        }
    }
</script>

<style scoped>
    .login-wrap{
        position: relative;
        width:100%;
        height:100%;
        background-image: url(../../assets/login-bg.jpg);
        background-size: 100%;
    }
    .ms-title{
        width:100%;
        line-height: 50px;
        text-align: center;
        font-size:20px;
        color: #000;
        border-bottom: 1px solid #ddd;
    }
    .ms-login{
        position: absolute;
        left:50%;
        top:50%;
        width:350px;
        margin:-190px 0 0 -175px;
        border-radius: 5px;
        background: rgba(255,255,255, 0.3);
        overflow: hidden;
    }
    .ms-content{
        padding: 30px 30px;
    }
    .login-btn{
        text-align: center;
    }
    .login-btn button{
        width:100%;
        height:36px;
        margin-bottom: 10px;
    }
    .login-tips{
        font-size:12px;
        line-height:30px;
        color:#fff;
    }
</style>