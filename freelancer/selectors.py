# XPath for project links on search results (a[1]..a[20] under first result card)
PROJECT_LINKS_BASE_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-search/app-search-projects/div/fl-container/div/div[2]/"
    "app-search-results/fl-card/div/div[2]/app-search-results-projects/div"
)
PROJECT_LINKS_MAX = 20

# XPath for project view page (title and description)
PROJECT_VIEW_TITLE_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-header/div/fl-container[1]/fl-grid/fl-col[1]/div/"
    "app-project-title/h1/span[2]"
)
PROJECT_VIEW_DETAILS_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-details/fl-page-layout/fl-container/fl-page-layout-single/"
    "fl-grid/fl-col[1]/app-project-details-card/fl-card/div/div/"
    "app-project-details-description/div"
)

# Bid form (project view)
BID_TEXTAREA_XPATH = '//*[@id="descriptionTextArea"]'
# Question area: container that lists existing questions (check for user id in descendants)
QUESTION_AREA_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-details/fl-page-layout/fl-container/fl-page-layout-single/"
    "fl-grid/fl-col[1]/app-project-clarification-board/fl-card/div/div/fl-comments"
)
QUESTION_TEXTAREA_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-details/fl-page-layout/fl-container/fl-page-layout-single/"
    "fl-grid/fl-col[1]/app-project-clarification-board/fl-card/div/div/"
    "fl-comments/fl-comments-form/div/div/div/fl-auto-complete/"
    "fl-auto-complete-rich-text/fl-auto-complete-input/fl-textarea/textarea"
)
QUESTION_SUBMIT_BUTTON_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-details/fl-page-layout/fl-container/fl-page-layout-single/"
    "fl-grid/fl-col[1]/app-project-clarification-board/fl-card/div/div/"
    "fl-comments/fl-comments-form/div/div/div[2]/div/fl-button[2]/button"
)
BID_SUBMIT_BUTTON_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-details/fl-page-layout/fl-container/fl-page-layout-single/"
    "fl-grid/fl-col[1]/app-project-details-freelancer/app-bid-form/fl-card/"
    "div/div[2]/div[2]/fl-button/button"
)

# After submitting bid: message shown when bid is inconsistent with profile
BID_INCONSISTENT_MESSAGE_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-proposals-wrapper/app-project-view-proposals/fl-page-layout/"
    "fl-container/fl-page-layout-single/fl-grid/fl-col[1]/"
    "app-bid-list-filtering-wrapper/app-bid-list/div/div/div[2]/div/h1/span[1]"
)
BID_INCONSISTENT_MESSAGE_TEXT = "Your bid appears inconsistent with your profile"
RETRACT_BID_BUTTON_XPATH = (
    "/html/body/app-root/app-logged-in-shell/div/fl-container/main/div/"
    "app-project-view/app-project-view-logged-in-wrapper/app-project-view-logged-in/"
    "app-project-view-proposals-wrapper/app-project-view-proposals/fl-page-layout/"
    "fl-container/fl-page-layout-single/fl-grid/fl-col[1]/"
    "app-bid-list-filtering-wrapper/app-bid-list/div/div/div[3]/app-bid-card/fl-card/"
    "div/div/fl-bid-pattern-card/div/div[2]/div[2]/fl-bid-pattern-card-actions/"
    "app-bid-card-actions-pattern/div[2]/div/fl-button[1]/button"
)
RETRACT_BID_CONFIRM_BUTTON_XPATH = (
    "/html/body/app-root/fl-modal/div/div/div/ng-component/div/div/fl-button[2]/button"
)
