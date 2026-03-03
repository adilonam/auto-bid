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
