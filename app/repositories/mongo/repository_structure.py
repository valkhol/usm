from app.constants import ModelType

repo_structure = {
    ModelType.POST.value: {
        ModelType.COMMENT.value: 'post',
        ModelType.STRIP.value: 'post',
    },
    ModelType.USER.value: {
        ModelType.FOLLOWER.value: 'id',
        ModelType.FOLLOWER.value: 'follow',
        ModelType.STRIP.value: 'user',
        ModelType.POST.value: 'user',
        ModelType.COMMENT.value: 'user',
    },
}
