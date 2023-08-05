<template>
    <el-dialog :title="$t('label.modifyPassword')" :visible.sync="dialogFormVisible" :before-close="handleClose"> 
      <el-form :model="changePasswordForm" :rules="rules" ref="changePasswordForm" :label-width="formLabelWidth">
        <el-form-item :label="$t('label.originalPassword')" prop="password">
          <el-input type="password" v-model="changePasswordForm.password" :placeholder="$t('message.inputOriginalPassword')" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item :label="$t('label.newPassword')" prop="new_password">
          <el-input type="password" v-model="changePasswordForm.new_password" :placeholder="$t('message.inputNewPassword')" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item :label="$t('label.confirmNewPassword')" prop="confirm_new_password">
          <el-input type="password" v-model="changePasswordForm.confirm_new_password" :placeholder="$t('message.inputConfirmNewPassword')" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="clear()">{{ $t('label.cancel') }}</el-button>
        <el-button type="primary" @click="submitForm('changePasswordForm')">{{ $t('label.confirm') }}</el-button>
      </div>
    </el-dialog>
</template>
<script>
  import { Message } from 'element-ui'

  export default {
    data(){
      return {
         changePasswordForm: {
            password: '',
            new_password: '',
            confirm_new_password: '',
         },
         formLabelWidth: '20%',
         dialogFormVisible: this.showChangePwdPopup,
      }
    },
    computed: {
      rules() {
          let calRules = {
              password: [
                  { required: true, message: this.$t('message.inputOriginalPassword'), trigger: 'blur' }
              ],
              new_password: [
                  { required: true, message:this.$t('message.inputNewPassword'), trigger: 'blur' },
                  { validator: this.validateNewPassword, message: this.$t('message.newPasswordSameAsPassword'), trigger: 'blur' },
              ],
              confirm_new_password: [
                  { required: true, message: this.$t('message.inputConfirmNewPassword'), trigger: 'blur' },
                  { validator: this.validateConfirmPassword, message: this.$t('message.confirmNewPasswordNotConsist'), trigger: 'blur' },
              ],
          }
          return calRules
      }
    },
    props:['showChangePwdPopup'],
    watch: {
      showChangePwdPopup: function(newVal, oldVal) {
          this.dialogFormVisible = newVal
      },
      dialogFormVisible: function(newVal, oldVal) {
          this.$bus.$emit("update:showChangePwdPopup", newVal)
      },
    },
    methods:{
      validateNewPassword(rule, value, callback) {
        if (value === this.changePasswordForm.password) {
            callback(new Error(this.$t('message.newPasswordSameAsPassword')));
        } else {
            callback();
        }
      },
      validateConfirmPassword(rule, value, callback) {
        if (value !== this.changePasswordForm.new_password) {
            callback(new Error(this.$t('message.confirmNewPasswordNotConsist')));
        } else {
            callback();
        }
      },
      handleClose(done) {
        this.$confirm(this.$t('message.confirmClose'))
          .then(_ => {
            this.clear();
            done();
          })
          .catch(_ => {});
      },
      clear() {
        this.changePasswordForm.password = ""
        this.changePasswordForm.new_password = ""
        this.changePasswordForm.confirm_new_password = ""
        this.dialogFormVisible = false
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
            if (valid) {
              this.$easyauth.authentication.changePassword(this.changePasswordForm.password, this.changePasswordForm.new_password)
                .then(res => {
                    this.dialogFormVisible = false
                    this.$store.commit("clearLoginUser")
                    this.$router.replace({
                                path: '/login',
                                query: { redirect: this.$router.currentRoute.fullPath }
                                });
                })
                .catch(err => {
                    Message.error({
                        message: [this.$t("message.changePasswordFailed"), ': ', err.data.detail].join("")
                })
              })
            } else {
              return false;
            }
        });
      },
    },
  }
</script>
