const loadPage = (page) => {
    return () => import(`@/views/dashboard/pages/${page}.vue`);
};

export default { loadPage };