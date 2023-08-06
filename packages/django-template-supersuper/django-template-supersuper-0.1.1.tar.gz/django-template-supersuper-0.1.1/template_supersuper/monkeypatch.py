import django.template.loader_tags
from django.template.loader_tags import (
    BLOCK_CONTEXT_KEY,
    BlockNode as OriginalBlockNode,
)


class BlockNode(OriginalBlockNode):

    def super_super(self):
        popped = self.context.render_context.get(BLOCK_CONTEXT_KEY).pop(self.name)
        value = self.super()
        self.context.render_context.get(BLOCK_CONTEXT_KEY).push(self.name, popped)
        return value


def doit():
    django.template.loader_tags.BlockNode = BlockNode
