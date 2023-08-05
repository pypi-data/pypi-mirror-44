<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-group"></i> {{ $t("page.roleAdminTitle") }}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button-group>
                    <el-button type="primary" icon="el-icon-plus" class="handle-create mr10" @click="handleCreate">{{ $t("label.create") }}</el-button>
                    <el-button type="danger" icon="el-icon-delete" :disabled="multipleSelection.length == 0" class="handle-del mr10" @click="handleDeleteAll">{{ $t("label.batchDelete") }}</el-button>
                    <el-button type="success" icon="el-icon-refresh" class="handle-refresh mr10" @click="getData">{{ $t("label.refresh") }}</el-button>
                </el-button-group>

                <el-button type="primary" icon="el-icon-search" style="float:right" @click="search"> {{ $t('label.search') }} </el-button>
                <el-input v-model="inputSearchWord" :placeholder="$t('placeholder.search')" class="handle-input mr10" style="float:right"></el-input>
            </div>
            <el-table :data="data" border class="table" ref="multipleTable"
             @selection-change="handleSelectionChange"
             :default-sort = "{prop: 'id', order: 'ascending'}"
             @sort-change="handleSortChange"
             stripe>
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column prop="id" label="ID" width="80" sortable="custom" fixed>
                </el-table-column>
                <el-table-column prop="last_name" :label="$t('label.name')" sortable="custom" :formatter="fullNameFormatter" width="100">
                </el-table-column>
                <el-table-column prop="phone" :label="$t('label.phone')" sortable="custom" width="120">
                </el-table-column>
                <el-table-column prop="date_joined" :label="$t('label.dateJoined')" sortable="custom" :formatter="dateJoinedFormatter" width="180">
                </el-table-column>
                <!--
                <el-table-column prop="is_staff" :label="$t('label.isStaff')" sortable="custom" :formatter="isStaffFormatter" width="120">
                </el-table-column>
                -->
                <el-table-column prop="is_active" :label="$t('label.isActive')" sortable="custom" :formatter="isActiveFormatter" width="120">
                </el-table-column>
                <el-table-column prop="roles" :label="$t('label.roles')" :formatter="rolesColumnFormatter">
                </el-table-column>
				<!--
                <el-table-column prop="user_permissions" :label="$t('label.privileges')" :formatter="permissionsColumnFormatter">
                </el-table-column>
				-->
                <el-table-column prop="last_login" :label="$t('label.lastLogin')" sortable="custom" :formatter="lastLoginFormatter" width="180">
                </el-table-column>
                <el-table-column :label="$t('label.operations')" width="100" align="center">
                    <template slot-scope="scope">
                        <el-button type="text" :title="$t('label.edit')" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)"></el-button>
                        <el-button type="text" :title="$t('label.resetPassword')" icon="el-icon-lx-edit" @click="handleResetPassword(scope.$index, scope.row)" :disabled="resetPasswordDisable(scope.row)"></el-button>
                        <el-button type="text" :title="$t('label.delete')" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)"></el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination background @current-change="handleCurrentChange"
                 @size-change="handleSizeChange"
                 layout="total, sizes, prev, pager, next, jumper"
                 :page-size='page_size' :total="totalPage" :current-page=cur_page
                 :page-sizes="[10, 20, 30, 50, 100]">
                </el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog :title="this.idx == -1 ? $t('label.create') : $t('label.edit')" :visible.sync="editUserVisible" width="60%">
            <el-form ref="form" :model="form" label-width="50px">
                <el-form-item label="ID" :label-width="formLabelWidth" v-show="form.id > 0">
                    {{ form.id }}
                </el-form-item>
                <el-form-item :label="$t('label.lastName')" :label-width="formLabelWidth">
                    <el-input v-model="form.last_name"></el-input>
                </el-form-item>
                <el-form-item :label="$t('label.firstName')" :label-width="formLabelWidth">
                    <el-input v-model="form.first_name"></el-input>
                </el-form-item>
                <el-form-item :label="$t('label.phone')" :label-width="formLabelWidth">
                    <el-input v-model="form.phone"></el-input>
                </el-form-item>
                <!--
                <el-form-item :label="$t('label.isStaff')" :label-width="formLabelWidth">
                    <el-checkbox v-model="form.is_staff"></el-checkbox>
                </el-form-item>
                -->
                <el-form-item :label="$t('label.isActive')" :label-width="formLabelWidth">
                    <el-checkbox v-model="form.is_active"></el-checkbox>
                </el-form-item>
                <el-form-item :label="$t('label.roles')" :label-width="formLabelWidth">
                    <div class="container">
                        <div class="drag-box">
                            <div class="drag-box-item">
                                <div class="item-title">{{ $t("label.selected") }}</div>
                                <draggable v-model="form.groups" :options="dragOptions">
                                    <transition-group tag="div" id="selectedGroups" class="item-ul">
                                        <div v-for="item in form.groups" class="drag-list" :key="item.id">
                                            {{item.name}}
                                        </div>
                                    </transition-group>
                                </draggable>
                            </div>
                            <div class="drag-box-item">
                                <div class="item-title">{{ $t("label.selections") }}</div>
                                <draggable v-model="form.availableGroups" :options="dragOptions">
                                    <transition-group tag="div" id="availableGroups" class="item-ul">
                                        <div v-for="item in form.availableGroups" class="drag-list" :key="item.id">
                                            {{item.name}}
                                        </div>
                                    </transition-group>
                                </draggable>
                            </div>
                        </div>
                    </div>
                </el-form-item>
				<!-- don't expose the interface for assigning permissions to an user, only allow assigning roles to an user
                <el-form-item :label="$t('label.privileges')" :label-width="formLabelWidth">
                    <div class="container">
                        <div class="drag-box">
                            <div class="drag-box-item">
                                <div class="item-title">{{ $t("label.selected") }}</div>
                                <draggable v-model="form.user_permissions" :options="dragOptions">
                                    <transition-group tag="div" id="selectedPermissions" class="item-ul">
                                        <div v-for="item in form.user_permissions" class="drag-list" :key="item.id">
                                            {{item.codename}}
                                        </div>
                                    </transition-group>
                                </draggable>
                            </div>
                            <div class="drag-box-item">
                                <div class="item-title">{{ $t("label.selections") }}</div>
                                <draggable v-model="form.availablePermissions" :options="dragOptions">
                                    <transition-group tag="div" id="availablePermissions" class="item-ul">
                                        <div v-for="item in form.availablePermissions" class="drag-list" :key="item.id">
                                            {{item.codename}}
                                        </div>
                                    </transition-group>
                                </draggable>
                            </div>
                        </div>
                    </div>
                </el-form-item>
				-->

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editUserVisible = false">{{ $t("label.cancel") }}</el-button>
                <el-button type="primary" @click="saveEdit">{{ $t("label.confirm") }}</el-button>
            </span>
        </el-dialog>

        <!-- 重置密码提示框 -->
        <el-dialog :title="$t('label.prompt')" :visible.sync="resetUserPwdVisible" width="500px" center>
            <div class="del-dialog-cnt">{{ $t("message.resetUserPassword")}}: {{ (idx > -1) ? this.tableData[this.idx][this.$projConfig.loginFieldName] : '' }}?</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetUserPwdVisible = false">{{ $t("label.cancel") }}</el-button>
                <el-button type="primary" @click="resetUserPwd">{{ $t("label.confirm") }}</el-button>
            </span>
        </el-dialog>

        <!-- 删除提示框 -->
        <el-dialog :title="$t('label.prompt')" :visible.sync="delUserVisible" width="500px" center>
            <div class="del-dialog-cnt">{{ $t("message.deleteWarning")}} {{ $t("label.user") }} {{ this.getDeleteUserNames() }}？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delUserVisible = false">{{ $t("label.cancel") }}</el-button>
                <el-button type="primary" @click="deleteRow">{{ $t("label.confirm") }}</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import draggable from 'vuedraggable'
    const maxRoleOrPermissionCountForShowInTable = 3
    const emptyForm = {
        id: -1,
        phone: '',
        first_name: '',
        last_name: '',
        is_active: true,
        is_staff: false,
        groups: [],
        availableGroups: [],
        user_permissions: [],
        availablePermissions: [],
    }
    export default {
        name: 'basetable',
        data() {
            return {
                tableData: [],
                cur_page: 1,
                page_size: 10,
                multipleSelection: [],
                inputSearchWord: '',
                searchWord: '',
                editUserVisible: false,
                delUserVisible: false,
                resetUserPwdVisible: false,
                userCount: 0,
                formLabelWidth: "20%",
                availablePermissions: [],
                availableGroups: [],
                form: JSON.parse(JSON.stringify(emptyForm)),
                idx: -1,
                sortProp: null,
                dragOptions:{
                    animation: 120,
                    scroll: true,
                    group: 'sortlist',
                    ghostClass: 'ghost-style'
                },
            }
        },
        created() {
            this.$easyauth.useradmin.getPermissions().then((res) => {
                this.availablePermissions = res.results;
            }).catch(err => {
                this.$message.error(`${this.$t("label.permission")} ${this.$t("message.retreiveFailed")}: ${this.$utils.logstr(err.data)}`)
            })

            this.$easyauth.useradmin.getRoles({page_size: 100000}).then((res) => {
                this.availableGroups = res.results;
            }).catch(err => {
                this.$message.error(`${this.$t("label.role")} ${this.$t("message.retreiveFailed")}: ${this.$utils.logstr(err.data)}`)
            })

            this.getData();
        },
        computed: {
            totalPage() {
                return this.userCount
            },
            data() {
                return this.tableData
            }
        },
        components:{
            draggable
        },
        methods: {
            // 分页导航
            handleCurrentChange(val) {
                this.resetIdx()
                this.cur_page = val;
                this.getData();
            },
            handleSizeChange(val) {
                this.resetIdx()
                this.page_size = val;
                this.getData();
            },
            resetIdx() {
                this.idx = -1
            },
            clearMultipleSelection() {
                this.multipleSelection = []
            },
            clearForm() {
                this.form = JSON.parse(JSON.stringify(emptyForm))
            },
            resetPasswordDisable(row) {
                return !row.is_active
            },
            // 获取 role和permission 数据
            getData() {
                this.resetIdx()
                this.clearMultipleSelection()
                this.clearForm()
                this.inputSearchWord = this.searchWord
                var params = {page: this.cur_page, page_size: this.page_size}
                if (this.searchWord) {
                    params.search = this.searchWord
                }
                if (this.sortProp) {
                    var ordering = this.sortProp.prop
                    if (this.sortProp.order) {
                        if (this.sortProp.order != 'ascending') {
                            ordering = '-' + ordering
                        }
                        params.ordering = ordering
                    }
                }
                this.$easyauth.useradmin.getUsers(params).then((res) => {
                    this.userCount = res.count
                    this.tableData = res.results;
                }).catch(err => {
                    this.$message.error(`${this.$t("label.user")} ${this.$t("message.retreiveFailed")}: ${this.$utils.logstr(err.data)}`)
                })
            },
            fullNameFormatter(row, column) {
                var fullName = ''
                if (row.last_name) {
                    fullName += row.last_name
                }
                if (row.first_name) {
                    if (fullName) {
                        fullName += ' '
                    }
                    fullName += row.first_name
                }
                return fullName
            },
            dateJoinedFormatter(row, column) {
                return this.$utils.date.formatLocaleDateTime(row.date_joined)
            },
            lastLoginFormatter(row, column) {
                 return this.$utils.date.formatLocaleDateTime(row.last_login)
            },
            isStaffFormatter(row, column) {
                if (row.is_staff) {
                    return this.$t("label.regular")
                } else {
                    return this.$t("label.outSource")
                }
            },
            isActiveFormatter(row, column) {
                if (row.is_active) {
                    return this.$t("label.active")
                } else {
                    return this.$t("label.disabled")
                }
            },
            permissionsColumnFormatter(row, column) {
                var permissionsStr = ""
                var i = 0
                if (row.user_permissions) {
                    row.user_permissions.forEach(p => {
                        if (++i > maxRoleOrPermissionCountForShowInTable) {
                            return;
                        }
                        permissionsStr += p.codename + ', '
                    })
                }
                if (permissionsStr) {
                    permissionsStr = permissionsStr.substring(0, permissionsStr.length - 2)
                }
                if (i > maxRoleOrPermissionCountForShowInTable) {
                    permissionsStr += " ..."
                }
                return permissionsStr
            },
            rolesColumnFormatter(row, column) {
                var rolesStr = ""
                var i = 0
                if (row.is_superuser) {
                    rolesStr += this.$t("label.superUser") + ', '
                    i ++
                }
                if (row.groups) {
                    row.groups.forEach(r => {
                        if (++i > maxRoleOrPermissionCountForShowInTable) {
                            return;
                        }
                        rolesStr += r.name + ', '
                    })
                }
                if (rolesStr) {
                    rolesStr = rolesStr.substring(0, rolesStr.length - 2)
                }
                if (i > maxRoleOrPermissionCountForShowInTable) {
                    rolesStr += " ..."
                }
                return rolesStr
            },
            search() {
                this.searchWord = this.inputSearchWord;
                this.cur_page = 1
                this.getData()
            },
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            handleCreate(index, row) {
                this.resetIdx()
                this.clearForm()
                this.form.availableGroups = this.getAvailableGroups(this.form.groups)
                this.form.availablePermissions = this.getAvailablePermissions(this.form.user_permissions)
                this.editUserVisible = true;
            },
            handleEdit(index, row) {
                this.idx = index;
                this.form = {
                    id: row.id,
                    phone: row.phone,
                    first_name: row.first_name,
                    last_name: row.last_name,
                    is_active: row.is_active,
                    is_staff: row.is_staff,
                    groups: row.groups,
                    availableGroups: this.getAvailableGroups(row.groups),
                    user_permissions: row.user_permissions,
                    availablePermissions: this.getAvailablePermissions(row.user_permissions)
                }
                this.editUserVisible = true;
            },
            handleResetPassword(index, row) {
                this.idx = index;
                this.resetUserPwdVisible = true;
            },
            getAvailableGroups(groups) {
                return this.availableGroups.filter(group =>{
                        var contains = false
                        groups.forEach(selectedGroup => {
                            if (selectedGroup.id == group.id) {
                                contains = true
                                return
                            }
                        })
                        if (!contains) {
                           return group
                        }
                    })
            },
            getAvailablePermissions(permissions) {
                return this.availablePermissions.filter(permission =>{
                        var contains = false
                        permissions.forEach(selectedPermossion => {
                            if (selectedPermossion.id == permission.id) {
                                contains = true
                                return
                            }
                        })
                        if (!contains) {
                           return permission
                        }
                    })
            },
            handleDelete(index, row) {
                this.idx = index;
                this.delUserVisible = true;
            },
            handleDeleteAll(index, row) {
                this.resetIdx()
                if (this.multipleSelection.length > 0) {
                    this.delUserVisible = true;
                }
            },
            getDeleteUserNames() {
                if (this.idx > -1) {
                    return '"' + this.tableData[this.idx][this.$projConfig.loginFieldName] + '"'
                } else if (this.multipleSelection.length > 0) {
                    var roles = ""
                    var maxShowCount = 3
                    var count = 0
                    this.multipleSelection.forEach(item => {
                        if (++ count > maxShowCount) {
                            roles += "..."
                            return
                        } else if (count > 1) {
                            roles += ", "
                        }
                        roles += item[this.$projConfig.loginFieldName]
                    })
                    return '"' + roles + '"'
                }
                return ''
            },
            delAll() {
                var removeIds = []
                var failedCount = 0
                var selectedCount = this.multipleSelection.length
                var delUserNames = this.getDeleteUserNames()
                this.multipleSelection.forEach(item => {
                    this.$easyauth.useradmin.deleteUser(item.id).then((res) => {
                        removeIds.push(item.id)
                        if (removeIds.length + failedCount == selectedCount) {
                            removeIds.forEach(i => {
                                this.tableData.some((d, index) => {
                                    if (d.id == i) {
                                        this.tableData.splice(index, 1)
                                        return
                                    }
                                })
                            })
                            this.$message.success(`${this.$t("label.user")} "${delUserNames}" ${this.$t("message.deleteSuccessfully")}`)
                        }
                    }).catch(err => {
                        failedCount ++
                        this.$message.error(`${this.$t("label.user")} ${item[this.$projConfig.loginFieldName]} ${this.$t("message.deleteFailed")}: ${this.$utils.logstr(err.data)}`)
                        if (removeIds.length + failedCount == selectedCount) {
                            removeIds.forEach(i => {
                                this.tableData.some((d, index) => {
                                    if (d.id == i) {
                                        this.tableData.splice(index, 1)
                                        return
                                    }
                                })
                            })
                        }
                    })
                })
                this.resetIdx()
                this.clearForm()
                this.clearMultipleSelection()
            },
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            handleSortChange(val) {
                if (!val.prop || !val.order) {
                    this.sortProp = null
                } else {
                    this.sortProp = val
                }
                this.resetIdx()
                this.cur_page = 1
                this.getData()
            },
            // 保存编辑
            saveEdit() {
                if (this.form.id > 0) {
                    var changeProps = {}
                    for (var key in this.form) {
                        if (key != 'id' && key != 'availableGroups' && key != 'availablePermissions') {
                            changeProps[key] = this.form[key]
                        }
                    }
                    this.$easyauth.useradmin.editUser(this.form.id, changeProps)
                    .then((res) => {
                        this.$set(this.tableData, this.idx, this.form);
                        this.resetIdx()
                        this.$message.success(`${this.$t("label.user")} ${this.form.id} ${this.$t('message.modifySuccessfully')}`);
                        this.clearForm()
                    }).catch(err => {
                        this.$message.error(`${this.$t("label.user")} ${this.form.id} ${this.$t("message.modifyFailed")}: ${this.$utils.logstr(err.data)}`)
                    })
                } else {
                    var newUser = {}
                    for (var key in this.form) {
                        if (key != 'id' && key != 'availableGroups' && key != 'availablePermissions') {
                            newUser[key] = this.form[key]
                        }
                    }
                    this.$easyauth.useradmin.createUser(newUser)
                    .then((res) => {
                        this.resetIdx()
                        this.$message.success(`${this.$t("label.user")} ${this.form[this.$projConfig.loginFieldName]}  ${this.$t('message.createSuccessfully')}`);
                        this.clearForm()
                        this.getData()
                    }).catch(err => {
                        this.$message.error(`${this.$t("label.user")} ${this.form[this.$projConfig.loginFieldName]} ${this.$t("message.createFailed")}: ${this.$utils.logstr(err.data)}`)
                    })
                }
                this.editUserVisible = false;
            },
            resetUserPwd() {
                if (this.idx > -1) {
                    var resetRow = this.tableData[this.idx];
                    this.$easyauth.useradmin.resetUserPwd(resetRow.id).then((res) => {
                        this.resetIdx()
                        this.$message.success(`${this.$t("label.user")} ${resetRow[this.$projConfig.loginFieldName]}  ${this.$t('message.resetUserPasswordSuccessfully')}`);
                    }).catch(err => {
                        this.$message.error(`${this.$t("label.user")} ${resetRow[this.$projConfig.loginFieldName]} ${this.$t("message.resetUserPasswordFailed")}: ${this.$utils.logstr(err.data)}`)
                    })
                }
                this.resetUserPwdVisible = false;
            },
            // 确定删除
            deleteRow() {
                if (this.idx > -1) {
                    var delRow = this.tableData[this.idx];
                    this.$easyauth.useradmin.deleteUser(delRow.id).then((res) => {
                        this.tableData.splice(this.idx, 1);
                        this.resetIdx()
                        this.$message.success(`${this.$t("label.user")} ${delRow[this.$projConfig.loginFieldName]}  ${this.$t('message.deleteSuccessfully')}`);
                    }).catch(err => {
                        this.$message.error(`${this.$t("label.user")} ${delRow[this.$projConfig.loginFieldName]} ${this.$t("message.deleteFailed")}: ${this.$utils.logstr(err.data)}`)
                    })
                } else if (this.multipleSelection.length > 0) {
                    this.delAll()
                }
                this.delUserVisible = false;
            }
        }
    }

</script>

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }
    .del-dialog-cnt{
        font-size: 16px;
        text-align: center
    }
    .table{
        width: 100%;
        font-size: 14px;
    }
    .red{
        color: #ff0000;
    }
     .drag-box{
        display: flex;
        user-select: none;
    }
    .drag-box-item {
        flex: 1;
        max-width: 330px;
        min-width: 300px;
        background-color: #eff1f5;
        margin-right: 16px;
        border-radius: 6px;
        border: 1px #e1e4e8 solid;
    }
    .item-title{
        padding: 8px 8px 8px 12px;
        font-size: 14px;
        line-height: 1.5;
        color: #24292e;
        font-weight: 600;
    }
    .item-ul{
        padding: 0 8px 8px;
        height: 260px;
        overflow-y: scroll;
    }
    .item-ul::-webkit-scrollbar{
        width: 0;
    }
    .drag-list {
        border: 1px #e1e4e8 solid;
        padding: 10px;
        margin: 5px 0 10px;
        list-style: none;
        background-color: #fff;
        border-radius: 6px;
        cursor: pointer;
        -webkit-transition: border .3s ease-in;
        transition: border .3s ease-in;
    }
    .drag-list:hover {
        border: 1px solid #20a0ff;
    }
    .drag-title {
        font-weight: 400;
        line-height: 25px;
        margin: 10px 0;
        font-size: 22px;
        color: #1f2f3d;
    }
    .ghost-style{
        display: block;
        color: transparent;
        border-style: dashed
    }
</style>
