from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsCreationOfExpirableLinkAllowedOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        result = super(IsCreationOfExpirableLinkAllowedOrReadOnly, self).has_permission(request, view)
        if not result:
            return result
        return request.user.account_plan_assignement.account_plan.can_create_expirable_links
